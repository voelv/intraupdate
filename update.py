import requests
#from bs4 import BeautifulSoup
from settings import settings
import logging

#Init logging
time_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO,filename='intraupdate.log', encoding='utf-8',format=f'%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt=time_format)

url = settings["intra"]["url"]+settings["intra"]["login_path"]

# Create a session with custom headers to preserve cookies and set User-Agent
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
session = requests.Session()
session.headers.update(headers)

def login():
    form_data = {}
    form_data["UserName"] = settings["intra"]["username"]
    form_data["Password"] = settings["intra"]["password"]

    session.post(url, data=form_data)

def logout():
    session.get(settings["intra"]["url"]+settings["intra"]["logout_path"])
    session.close()

if __name__ == "__main__":
    login()
    logout()

# # Make a GET request to retrieve the form
# response = session.get(url)
# html_content = response.text

# # Use BeautifulSoup to parse the HTML content
# soup = BeautifulSoup(html_content, 'html.parser')

# # Find the form on the page
# form = soup.find('form')

# # Extract form inputs, including hidden fields, and build data dictionary with desired values
# form_data = {}
# for input_tag in form.find_all('input'):
#     input_name = input_tag.get('name')
#     if input_name:
#         if 'value' in input_tag.attrs:
#             form_data[input_name] = input_tag['value']
#         else:
#             form_data[input_name] = 'your_value_here'

# # Make a POST request with the form data
# response = session.post(url, data=form_data)

# # Process the response as needed
# print(response.text)