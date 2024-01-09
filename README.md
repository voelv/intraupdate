# Intraupdate
## Gets data from Forældreintra using Selenium
This will eliminate the problem of javascript not being enabled, or missing data from lazy loaded pages on Foraeldreintra

### Selenium Customizables
- Download newest Selenium drivers on the fly or use local copies
- Choose Firefox or Chrome
- Pass parameters to Selenium

### Data from Foraeldreintra
- Get data from one or more children
- Ugeplaner
- Lektiebog

### Saving data
- Implemented with MySQL
- Setup script included

### How to Setup
- Review and change `settings.py`
- Run `db.setup()`

### Get and save data from Forældreintra to MySql database
- Run `update.py [db]`
Optional: [db] is either "test" or "prod"
Not supplying argument will use "test"
  
    
-- voelv@proton.me