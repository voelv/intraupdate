
from settings import settings
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from util import infomessage

mod_logger = logging.getLogger(__name__)

def log_in(browser):
    infomessage(mod_logger,"Loggin in")

    browser.get(settings["intra"]["url"])

    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "UserName")))

        browser.find_element("id", "UserName").send_keys(settings["intra"]["username"])
        # find password input field and insert password as well
        browser.find_element("id", "Password").send_keys(settings["intra"]["password"])
        # click login button
        #browser.find_element("type", "submit").click()
        browser.find_element(By.XPATH,"//input[@type='submit']").click()

        infomessage(mod_logger,"Loggin in succesful")
    except TimeoutException as e:
            logging.exception(e)

def log_out(browser):
    infomessage(mod_logger,"Loggin out")

    browser.get(settings["intra"]["url"]+settings["intra"]["logout_path"])

    infomessage(mod_logger,"Log out successful")
    infomessage(mod_logger,"Quitting browser")

    browser.quit() 

    infomessage(mod_logger,"Browser quit successfully")

