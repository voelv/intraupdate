# Intraupdate
## Gets data from Forældreintra using Selenium
This will eliminate the problem of javascript not being enabled, or missing data from lazy loaded pages on Foraeldreintra

### Selenium Customizables
- Download newest Selenium drivers on the fly or use local copies
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


-- voelv@proton.me