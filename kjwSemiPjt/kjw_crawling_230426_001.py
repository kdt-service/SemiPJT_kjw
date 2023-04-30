import requests
from bs4 import BeautifulSoup

log_info = {
    'id': 'KJY153',
    'pw': 'Caesar11!!'    
}

stock_codes = ['005930', '000100', '034720']

session = requests.Session()

login_page = session.get('https://www.samsungpop.com/login/sso.jsp')

soup = BeautifulSoup(login_page.text, 'html.parser')
login_form = soup.find('form')

inputs = login_form.findAll('input')

print(f'inputs: {inputs}')