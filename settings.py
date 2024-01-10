settings={
    #True: Output to console as well as log. False: Output to log only
    "verbose":True,
    "intra":{
        #URL for the specifik foraeldreintra. No trailing slash
        "url":"https://url-not-set.m.skoleintra.dk",
        #URL for the specific loginpath
        "login_path":"/Account/IdpLogin?partnerSp=urn%3Aitslearning%3Ansi%3Asaml%3A2.0%3A<####change this to match url#####>",
        "diary_url":"/parent/{}/{}item/weeklyplansandhomework/diary/notes/{}",
        "week_plan_url":"/parent/{}/{}item/weeklyplansandhomework/item/class/{}-{}",
        "logout_path":"/Account/LogOff",
        #Parent credentials
        "username":"<username not set>",
        "password":"<password not set>"
    },
    "children":{
        #One entry for each child
        "Name1":{
            #Get these values from the url on a specifik "Ugeplan"
            #example https://<URL for the specifik foraeldreintra>/parent/<id>/<Name>item/weeklyplansandhomework/diary/<diaryid>/2024-01-15"
            "firstname":"Name1",
            "id":9999,
            "diaryid":99
        },
        "Name2":{
            "firstname":"Name2",
            "id":1186,
            "diaryid":65
        }
    },
    "database":{
        #Precisly one entry for test and one entry for prod database.
        "test":{
            "host": "test db host not set",
            "user": "test db user not set",
            "password": "test db password not set",
            "database": "test db name not set",
        },
        "prod":{
            "host": "prod db host not set",
            "user": "prod db user not set",
            "password": "prod db password not se",
            "database": "prod db name not set",
        }
    },
    #Firstnames of chilren to update data for. Must match the firstnames in the "children" section
    "update":{
        "children":["Name1","Name2"]
    },
    "selenium":{
        # If set to True, local drive and browser must be present locally and will not be downloaded
        "local": True,
        # must be either 'chrome' or 'firefox'
        "type":"firefox",
        #"--no-sandbox"
        "arguments":{
            "chrome":["--headless=new","--disable-dev-shm-usage","--disable-extensions","--no-first-run","–allow-file-access-from-files"],
            "firefox":["--headless"]
        },
        "prefs":{
            "profile.managed_default_content_settings.images": 2
            },
        # set a portnumber as int or None type
        "port":8080,
        "driver_path":{
            "chrome":"<Path not set>/chromedriver.exe",
            "firefox":"<Path not set>/geckodriver.exe"},
        "browser_executable_path" : {
            "chrome":"<Path not set>/chrome.exe",
            "firefox":"<Path not set>/firefox.exe"
            }
    }
}