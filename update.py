import mechanize
from settings import settings
from homework import get as get_homework
import logging
import sys
from util import infomessage

#Init logging
time_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO,filename='intraupdate.log', encoding='utf-8',format=f'%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt=time_format)

# Create a Browser instance
def get_browser():
    br = mechanize.Browser()
    br.set_handle_robots(False)

    br.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
    return br

def login(br):
    infomessage(logging,"Logging in")
    # Load the login page 
    br.open(settings["intra"]["url"])

    # Select the first form (login form)
    br.select_form(nr=0)  
    
    # Fill out the form fields  
    br["UserName"] = settings["intra"]["username"]
    br["Password"] = settings["intra"]["password"]
    
    # Submit the form  
    br.submit()  

    # After ending on 'javascript not supported form' submit again  
    br.select_form(nr=0)  
    br.submit()
    infomessage(logging,"Login succesful")  

def logout(br):
    infomessage(logging,"Logging out")
    br.open(settings["intra"]["url"]+settings["intra"]["log_off_url"])
    infomessage(logging,"Logout successful")

    infomessage(logging,"Closing browser")
    br.close() 
    infomessage(logging,"Browser closed successfully")

if __name__ == "__main__":
    
    browser=get_browser()
    login(browser)
    print(get_homework(browser,"Storm"))
    #update_homework(browser)
    #update_weekplans(browser)
    logout(browser)
    infomessage(logging," -- :D Have a nice day :D -- ")
    sys.exit()

