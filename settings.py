settings={
    "verbose":True,
    "intra":{
        "url":"https://haslevprivatskole.m.skoleintra.dk",
        "login_path":"/Account/IdpLogin?partnerSp=urn%3Aitslearning%3Ansi%3Asaml%3A2.0%3Ahaslevprivatskole.m.skoleintra.dk",
        "diary_url":"/parent/{}/{}item/weeklyplansandhomework/diary/notes/{}",
        "week_plan_url":"/parent/{}/{}item/weeklyplansandhomework/item/class/{}-{}",
        "logout_path":"/Account/LogOff",
        "username":"petthe",
        "password":"f4nd4ng0"
    },
    "children":{
        "Oskar":{
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
    "host": "qantm.net",
    "user":"qantmnet_fam_production",
    "password": "Wizard-Nuzzle8-Landed",
    "database": "qantmnet_fam_PROD",
    },
    "update":{
        "children":["Oskar","Storm"]
    },
    "dash":{
        "homework":[1322,1186]
    },
    "verbose":True,
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
            "firefox":"C:/Users/pravnthers/Personlig/Fam/geckodriver.exe"},
        "browser_executable_path" : {
            "chrome":"C:/Program Files/Google/Chrome/Application/chrome.exe",
            "firefox":"C:/Program Files/Mozilla Firefox/firefox.exe"
            }
    }
}