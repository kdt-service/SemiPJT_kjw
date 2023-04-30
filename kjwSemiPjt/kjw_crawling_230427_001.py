import requests
from bs4 import BeautifulSoup

# HTTP GET Request
url = 'https://finance.naver.com/item/coinfo.naver?code=000100'
response = requests.get(url)

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 원하는 데이터 추출
table = soup.find('table', {'class': 'co_info'})
tbody = table.find('tbody')
tr = tbody.find('tr', {'class': 'strong'})
tds = tr.find_all('td')
name = tds[0].text.strip()  # 종목명
market = tds[1].text.strip()  # 시장구분
industry = tds[2].text.strip()  # 업종명

# 결과 출력
print(name, market, industry)
