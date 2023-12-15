from settings import settings
import logging
from bs4 import BeautifulSoup
from datetime import date
from util import fam_msg, is_after_now, intra_weekplan_date_is_today
from db import save_weekplan, get_latest

mod_logger = logging.getLogger(__name__)

def week_to_fetch(wk=None):
    #If its saturday or sunday and a specifik week number is not given, get next weeks plan
    if date.today().isoweekday() in [6,7] and not wk:
        week = date.today().isocalendar().week+1
    else:
        week = wk or date.today().isocalendar().week
    return week

def get_weekplan(browser, child_name :str, week_num=None, year=None):
    mod_logger.info(f"Getting weekplan for {child_name}")
    child=settings["children"][child_name]

    # determine which weeknum to fetch
    week_= week_to_fetch(week_num)

    # get year from param or set currentyear
    year_= year or date.today().year

    week_plan_url=settings["intra"]["url"]+settings["intra"]["week_plan_url"].format(child["id"],child["firstname"],week_,year_)

    browser.get(week_plan_url)

    try:
        # Check the page is loading
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sk-weekly-plan-row")))
        content = browser.page_source
        soup = BeautifulSoup(content, 'html.parser')

        weekplan=[]
        
        # Get all rows
        # 1. row is general
        plan_rows=soup.find_all("div", class_="sk-weekly-plan-row")
        
        for day in plan_rows:
            day_name=day.find("span", class_="sk-weekly-plan-day").contents[0]
            day_date=day.find("span", class_="sk-weekly-plan-date").contents[0] if day.find("span", class_="sk-weekly-plan-date") else None
            day_subjects=day.find_all("span", class_="sk-weekly-plan-subject")

            # clean up results by removing tags newlines and spaces
            day_subjects=[ele.text.strip() for ele in day_subjects if ele.text] if day_subjects else ["Intet emne"]

            day_subject_contents=day.find_all("span", class_="sk-weekly-plan-content sk-user-input") if day.find_all("span", class_="sk-weekly-plan-content sk-user-input") else []

            # clean up
            day_subject_contents=[ele.text.strip() for ele in day_subject_contents if ele] if day_subject_contents else []


            # put together subjects and content
            d=dict(zip(day_subjects, day_subject_contents))

            mod_logger.debug("subjects:",day_subjects)
            mod_logger.debug("contents:",day_subject_contents,"\n")

            dayplan={"name":day_name,"date":day_date,"plan":d}

            weekplan.append(dayplan)

        w={"name":child_name, "weekplan":weekplan}

        return w
    
    except IndexError as ie:
        mod_logger.error(ie)
    except TimeoutException as te:
        mod_logger.exception(te)
    except Exception as e:
        mod_logger.exception(e)
    

def print_weekplan(weekplan :list, later=True):
    for day in weekplan:
        strdate= day["date"] or ""
        if strdate:
            if is_after_now(strdate):
                print(f"{day['name']} {strdate}")
                for key,value in day["plan"].items():
                    print(key,"\n",value)


def get_intra_weekplan_list(browser, children :list):
    """Returns a list of homework for each child suplied in the 'children' list"""
    num_c=len(children)
   # logging.info("Getting {} children".format(num_c))
    weekplan=[]

    try:
        for i,child in enumerate(children):
            fam_msg("Getting plan {} of {}".format(i+1,num_c), mod_logger)
            s=get_weekplan(browser, child)
            weekplan.append(s)
    except Exception as e:
        mod_logger.exception(e)
    else:
        fam_msg("Succesfully retrieved {} plans".format(num_c), mod_logger)
        return weekplan


def update(browser):
    wp=get_intra_weekplan_list(browser,settings["update"]["children"])
    save_weekplan(wp)


def today(weekplans :list)->list:
    """Takes a list of weekplans and filters them to return only the plan for today"""
    for plan in weekplans:
        plan["weekplan"] = [ele for ele in plan["weekplan"] if ele["date"] and intra_weekplan_date_is_today(ele["date"])]

    return weekplans

def load(today_=False):
    try:
        wp=get_latest("weekplan", settings["dash"]["homework"])
    except Exception as ex:
        fam_msg(ex,mod_logger)

    if today_:
        return today(wp)
    else:
        return wp


