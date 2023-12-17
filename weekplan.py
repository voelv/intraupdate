from settings import settings
import logging
from util import infomessage
from bs4 import BeautifulSoup
from datetime import date

#from util import fam_msg, is_after_now, intra_weekplan_date_is_today
#from db import save_weekplan, get_latest

mod_logger = logging.getLogger(__name__)

def week_to_fetch(wk=None):
    #If its saturday or sunday and a specifik week number is not given, get next weeks plan
    if date.today().isoweekday() in [6,7] and not wk:
        week = date.today().isocalendar().week+1
    else:
        week = wk or date.today().isocalendar().week
    return week

def get_weekplan(browser, child_name :str, week_num=None, year=None):
    infomessage(mod_logger,f"Getting weekplan for {child_name}")
    child=settings["children"][child_name]

    # determine which weeknum to fetch
    week_= week_to_fetch(week_num)

    # get year from param or set currentyear
    year_= year or date.today().year

    week_plan_url=settings["intra"]["url"]+settings["intra"]["week_plan_url"].format(child["id"],child["firstname"],week_,year_)

    try:
        response = browser.open(week_plan_url)
        content = response.read()
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
    
    except IndexError as ie:
        mod_logger.error(ie)
        infomessage(mod_logger,f"An error occured see log")
        return None

    except Exception as e:
        mod_logger.exception(e)
        infomessage(mod_logger,f"An exception occured see log")
        return None
    else:
        return w
    

def get_weekplans(browser, children :list):
    """Returns a list of homework for each child suplied in the 'children' list"""
    num_c=len(children)
   # logging.info("Getting {} children".format(num_c))
    weekplans=[]

    try:
        for i,child in enumerate(children):
            infomessage(mod_logger,"Getting plan {} of {}".format(i+1,num_c))
            s=get_weekplan(browser, child)
            weekplans.append(s)
    except Exception as e:
        mod_logger.exception(e)
        return None
    else:
        infomessage(mod_logger,"Succesfully retrieved {} plans".format(num_c))
        return weekplans


# def update(browser):
#     wp=get_weekplans(browser,settings["update"]["children"])
#     save_weekplan(wp)


# def today(weekplans :list)->list:
#     """Takes a list of weekplans and filters them to return only the plan for today"""
#     for plan in weekplans:
#         plan["weekplan"] = [ele for ele in plan["weekplan"] if ele["date"] and intra_weekplan_date_is_today(ele["date"])]

#     return weekplans

# def load(today_=False):
#     try:
#         wp=get_latest("weekplan", settings["dash"]["homework"])
#     except Exception as ex:
#         fam_msg(ex,mod_logger)

#     if today_:
#         return today(wp)
#     else:
#         return wp


