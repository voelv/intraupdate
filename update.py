import os
import sys
import logging
from selenium import webdriver
from actions import log_in,log_out
from homework import update as update_homework
from weekplan import update as update_weekplans
from util import infomessage
from db import get_connection

#Init logging
logging.basicConfig(level=logging.INFO,filename='intraupdate.log', encoding='utf-8',format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

#init selenium logger
sel_logger = logging.getLogger('selenium')
handler = logging.FileHandler("selenium.log")
sel_logger.addHandler(handler)
logging.getLogger('selenium.webdriver.remote').setLevel(logging.WARN)
logging.getLogger('selenium.webdriver.common').setLevel(logging.INFO)

#Get module logger
mod_logger = logging.getLogger(__name__)

# check if the settings file exists
settings_filename="settings.py"
if not os.path.exists(settings_filename):
    print(f"{settings_filename} was not found, update can not continue - exiting")
    print(os.path)
    logging.error("The settings file is not present, ending program")
    sys.exit()

from settings import settings

def init_browser():
    infomessage(mod_logger,"Initializing browser object")
    infomessage(mod_logger,"Browser type is {}".format(settings["selenium"]["type"]))

    if settings["selenium"]["local"]:
         infomessage(mod_logger,"Local files are used")
         infomessage(mod_logger,"Driver path: {}".format(settings["selenium"]["driver_path"][settings["selenium"]["type"]]))
         infomessage(mod_logger,"Binary path: {}".format(settings["selenium"]["browser_executable_path"][settings["selenium"]["type"]]))

    service_options={}
    try:
        service=None
        if settings["selenium"]["type"] == "firefox":

            from selenium.webdriver.firefox.service import Service
            options = webdriver.FirefoxOptions()

            infomessage(mod_logger,"Adding args: {}".format(settings["selenium"]["arguments"]["firefox"]))
            for arg in settings["selenium"]["arguments"]["firefox"]:
                options.add_argument(arg)
            
            service_options["port"]=settings["selenium"]["port"]
            
            if settings["selenium"]["local"]:
                service_options["executable_path"]=settings["selenium"]["driver_path"]["firefox"]
                options.binary_location=settings["selenium"]["browser_executable_path"]["firefox"]

            service = Service(**service_options)
            browser = webdriver.Firefox(service=service,options=options)
        
        # use Chrome as standard
        else:
            from selenium.webdriver.chrome.service import Service
            
            options = webdriver.ChromeOptions()
            options.experimental_options["prefs"] = settings["selenium"]["prefs"]
            options.page_load_strategy = "eager"

            infomessage(mod_logger,"Adding args: {}".format(settings["selenium"]["arguments"]["chrome"]))
            for arg in settings["selenium"]["arguments"]["chrome"]:
                options.add_argument(arg)


            if settings["selenium"]["port"]:
                options.add_argument("--remote-debugging-port={}".format(settings["selenium"]["port"]))

    
            if settings["selenium"]["local"]:
                service_options["executable_path"]=settings["selenium"]["driver_path"]["chrome"]
                options.binary_location = settings["selenium"]["browser_executable_path"]["chrome"]

            service = Service(**service_options)
            browser = webdriver.Chrome(service=service,options=options)
        
    except Exception as ex:
        infomessage(mod_logger,"An exception ocurred, see log")
        logging.exception(ex)
        sel_logger.exception(ex)
        sys.exit()
    else:
        return browser
    
if __name__ == "__main__":
    
    try:
        db_conn = get_connection()
    except Exception as ex:
        logging.exception(ex)
        infomessage(mod_logger,"An exception occurred connecting to the database. See log")
        sys.exit()
    else:
        try:
            browser=init_browser()
            log_in(browser)
            update_homework(browser, db_conn)
            update_weekplans(browser, db_conn)
            log_out(browser)

        except Exception as ex:
            infomessage(mod_logger,"An exception ocurred, see log")
            logging.exception(ex)
            sel_logger.exception(ex)
            sys.exit()

        else:
            if db_conn:
                db_conn.close()
            infomessage(mod_logger,"Intra data retrieved and stored successfully")

        finally:
            sys.exit()