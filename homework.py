from settings import settings
import logging
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from db import save_homework
from util import infomessage

mod_logger = logging.getLogger(__name__)

def get_intra_homework(browser, child_name :str):
    infomessage(mod_logger,"Getting {}".format(child_name))
    child=settings["children"][child_name]

    child_diary_url=settings["intra"]["url"]+settings["intra"]["diary_url"].format(child["id"],child["firstname"],child["diaryid"])

    browser.get(child_diary_url)

    try:
        # Check the page is loading
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "sk-diary-notes-container")))
        content = browser.page_source
        soup = BeautifulSoup(content, 'html.parser')
        notes_container=soup.find(attrs={'id':'sk-diary-notes-container'})
        notes_list=notes_container.findChild("ul")
        li_list=notes_list.findChildren("li")

        home_work_list=[]
        for li in li_list:
            # Each Li is a day entry
            home_work_day={}
            home_work_day["date"]=li.findChild("b").contents[0]
            table=li.findChild("table")
            table_body = table.find('tbody')

            #Each row is a subject that day, the first ro is skipped [1:]
            rows = table_body.findChildren('tr')
            home_work_subject_list_per_day=[]
            for row in rows[1:]:
                cols = row.findChildren('td')
                # if second cell is filled out, there is homework in that subject. The name of the subject is in the first row
                # check if there are actualy 2 columns in the row and thta there is some contet in the 2nd column 
                if len(cols) == 2 and len(cols[1].text.strip()) > 2:
                    cols = [ele.text.strip() for ele in cols]
                    home_work_subject_list_per_day.append(cols)

            home_work_day["home_work"]=home_work_subject_list_per_day
            home_work_list.append(home_work_day) 

        homework={"name":child_name, "homework":home_work_list}
        
        return homework
    
    except IndexError as ie:
        infomessage(mod_logger,"An error ocurred, see log")
        mod_logger.error(ie)
    except TimeoutException as te:
        infomessage(mod_logger,"A timeout exception ocurred, see log")
        mod_logger.exception(te)
    except Exception as e:
        infomessage(mod_logger,"An exception ocurred, see log")
        mod_logger.exception(e)
    

def get_intra_homework_list(browser, children :list):
    """Returns a list of homework for each child suplied in the 'children' list"""
    num_c=len(children)
   # logging.info("Getting {} children".format(num_c))
    homework=[]

    try:
        for i,child in enumerate(children):
            infomessage(mod_logger,"Getting child {} of {}".format(i+1,num_c))      
            s=get_intra_homework(browser, child)
            homework.append(s)
    except Exception as e:
        infomessage(mod_logger,"An exception ocurred, see log")
        mod_logger.exception(e)
    else:
        infomessage(mod_logger,"Succesfully retrieved data for {} children".format(num_c))
        return homework

def update(browser):
    hw=get_intra_homework_list(browser,settings["update"]["children"])
    save_homework(hw)

