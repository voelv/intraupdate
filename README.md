# Intraupdate
## Gets data from Forældreintra using Selenium
Scrape and store data from Forældreintra in MySql
Using Selenium til eliminate the problem of javascript not being enabled, or missing data from lazy loaded pages on Foraeldreintra
Modules like httpx and requests wil not be able to get the data properly, even wtih async.

### Selenium Customizables
- Download newest Selenium drivers on the fly or use local copies
  - Default is to use local Selenium driver and browser, so you must download these and enter the paths in `settings.py`
  - Alternatively change the setting `selenium.local` in `settings.py` to `False`
- Choose Firefox or Chrome
- Pass parameters to Selenium

### Data from Foraeldreintra
- Get data from one or more children
  - Ugeplan
  - Lektiebog

### Saving data
- Implemented with MySQL
- Setup script included

### How to Setup
- Review and change `settings.py`
- Run `db.setup()`

### Get and save data from Forældreintra to MySql database
- Run `update.py [db]`

Optional: [db] is either "test" or "prod".  
Not supplying argument will use "test".  
Example: `Python update.py prod`  
Change database properties in `settings.py`  
  
### Potential use
- Build a family dashboard with homework and weekplan data
- Send alerts by email or other communication platforms

### Tip
Create a .bat file and schedule the bat file to update data on a regular basis  
ex: ```cmd /k "cd /d c:\<path to your project>\.venv\Scripts & call .\activate.bat  & cd /d c:\<path to the update file> & python update.py <db>"```

### Disclaimer
This is a webscraper.
If at any point in time Forældre intra changes it's HTML, the code will have to be changed to reflect the new structure.


### Enjoy
-- voelv@proton.me