settings={
    #True: Output to console as well as log. False: Output to log only
    "verbose":True,
    "intra":{
        #URL for the specifik foraeldreintra. No trailing slash
        "url":"https://haslevprivatskole.m.skoleintra.dk",
        #URL for the specific loginpath
        "login_path":"/Account/IdpLogin?partnerSp=urn%3Aitslearning%3Ansi%3Asaml%3A2.0%3Ahaslevprivatskole.m.skoleintra.dk",
        "diary_url":"/parent/{}/{}item/weeklyplansandhomework/diary/notes/{}",
        "week_plan_url":"/parent/{}/{}item/weeklyplansandhomework/item/class/{}-{}",
        "logout_path":"/Account/LogOff",
        #Parent credentials
        "username":"petthe",
        "password":"f4nd4ng0"
    },
    "children":{
        #One entry for each child
        "Oskar":{
            #Get these values from the url on a specifik "Ugeplan"
            #example https://<URL for the specifik foraeldreintra>/parent/<id>/<firstname>item/weeklyplansandhomework/diary/<diaryid>/2024-01-15"
            "firstname":"Oskar",
            "id":1322,
            "diaryid":71
        },
        "Storm":{
            "firstname":"Storm",
            "id":1186,
            "diaryid":65
        }
    },
    "database":{
        #Precisly one entry for test and one entry for prod database.
        "test":{
            "host": "qantm.net",
            "user": "qantmnet_fam_develop",
            "password": "Broiler-Prancing6-Yippee",
            "database": "qantmnet_fam_TEST",
        },
        "prod":{
            "host": "qantm.net",
            "user": "qantmnet_fam_production",
            "password": "Wizard-Nuzzle8-Landed",
            "database": "qantmnet_fam_PROD",
        }
    },
    #Firstnames of chilren to update data for. Must match the firstnames in the "children" section
    "update":{
        "children":["Oskar","Storm"]
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
            "chrome":"C:/Users/pravnthers/Personlig/Fam/chromedriver.exe",
            "firefox":"C:/Users/pravnthers/Personlig/Intraupdate/intraupdate/geckodriver.exe"},
        "browser_executable_path" : {
            "chrome":"C:/Program Files/Google/Chrome/Application/chrome.exe",
            "firefox":"C:/Program Files/Mozilla Firefox/firefox.exe"
            }
    }
}