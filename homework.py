from bs4 import BeautifulSoup
from settings import settings
import logging
from util import infomessage

mod_logger=logging.getLogger(__name__)

def get(browser, child_name :str):

    child=settings["children"][child_name]

    child_diary_url=settings["intra"]["url"]+settings["intra"]["diary_url"].format(child["id"],child["firstname"],child["diaryid"])

    infomessage(mod_logger,f"Getting homework for {child_name}")

    try:
        content = browser.open(child_diary_url)
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

            home_work_day["home_work"]=home_work_subject_list_per_day/0
            home_work_list.append(home_work_day) 

        homework={"name":child_name, "homework":home_work_list}
 


    except IndexError as ie:
        mod_logger.error(ie)
        infomessage(mod_logger,f"An error occured ({ie.__cause__}) see log")
        return None

    except Exception as e:
        mod_logger.exception(e)
        infomessage(mod_logger,f"An exception occured ({e.__cause__}) see log")
        return None

    else:              
        infomessage(mod_logger,f"Homework for {child_name} retrieved") 
        return homework