from settings_local import settings
import datetime
import string
import random
import logging
import calendar

mod_logger=logging.getLogger(__name__)

verboseprint = print if settings["verbose"] else lambda *a, **k: None

def infomessage(logger,str):
    verboseprint("intraupdate:",str)
    logger.info(str)
 
def rand_id():
    # initializing size of string
    N = 7
    # using random.choices()
    # generating random strings
    res = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=N))
    return str(res)

def format_intra_date(str):
# Torsdag, 7. dec. 2023:'

    d=str.split(",")[1:][0][:-1].strip().split(".")
    date = datetime.date(int(d[2]),int(datetime.datetime.strptime(d[1].strip(),"%b").month),int(d[0]))
    return date

def intra_weekplan_date_is_today(str):
    """Test if the date is today. And if the date is in a weekend, """
    try:
        #todays date for reference
        date_now=datetime.date.today()
        #check if today is a weekend
        if datetime.date.today().isoweekday() in [6,7]:
            #If its weekend, use the following mondays date as 'now' by subtracting current days index from 8
            date_now = datetime.date.today() + datetime.timedelta(days=8-datetime.date.today().isoweekday())
        #convert string to date. However this will have 1900 as year
        d=datetime.datetime.strptime(str,"%d. %b.")
        # replace 1900 with current year
        d=datetime.date(date_now.year,d.month,d.day)
        return d == date_now 
    except Exception as ex:
        infomessage(mod_logger,"An exception ocurred see log")
        mod_logger.exception(ex)

def date_or_following_monday():
    today=datetime.date.today()
    if today.isoweekday() in [6,7]:
        #If its weekend, use the following mondays date as 'now' by subtracting current days index from 8
        return today + datetime.timedelta(days=8-today.isoweekday())
    else:
        return today

def earlier(date):
    return True if format_intra_date(date) < datetime.date.today() else False

def is_after_now(str_date):
    try:
        date_list=[ele.strip() for ele in str_date.split(".")]
        dictdd={month.lower(): index for index, month in enumerate(calendar.month_abbr) if month}
        day=int(date_list[0])
        month=dictdd[date_list[1]]
        today=datetime.date.today()
        year=int(today.year)

        date_to_check=datetime.date(year,month,day)

        if date_to_check >= today:
            return True
        else:
            return False
    except Exception as ex:
        infomessage(mod_logger,"An exception ocurred see log")
        mod_logger.exception(ex)
        return None

def validate_db_arg_input(args):
    if len(args)==1:
        return "test"
    elif len(args) == 2: 
        if args[1] == "test":
            return "test"
        elif args[1] == "prod":
            return "prod"
    else: 
        return "test"