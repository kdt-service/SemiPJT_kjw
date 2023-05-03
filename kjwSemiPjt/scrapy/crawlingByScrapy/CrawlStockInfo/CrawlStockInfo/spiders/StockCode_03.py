import requests
import pandas as pd
import scrapy
import os
import csv
import io
#from CrawlStockInfo.items import CrawlstockinfoItem

#1.상장법인목록 조회버튼 클릭 후 들어온 새 창 URL
url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage'

#2.POST 요청 데이터
data = {
    'currentPage': '1',
    'pageSize': '100',
    'searchType': '13',
    'industry': '',
    'fiscalYearEnd': 'all',
    'comAbbrvTmp': '',
    'location': 'all'
}

#3.POST 요청 보내기
response = requests.post(url, data=data)
results = response.text
print(f'\n\n 확인을 위한 출력 url :   {results}')


# #4.응답 데이터 JSON 파싱 후 DataFrame으로 변환
# data = response.json()
# df = pd.concat([pd.DataFrame(d) for d in data.values()])
# #excel_data = io.BytesIO(response.content)
# #df = pd.read_excel(excel_data)

# class StockCodeSpider(scrapy.Spider):
#     name = 'stockcode_03'
#     allowed_domains = ['kind.krx.co.kr']
#     start_urls = ['https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage']
    
#     def parse(self, response):
#         #새창을 열기 위해 JavaScript코드를 추출
#         open_popup_js = response.css('a.btn2::attr(onclick)').extract_first()
#         #JavaScript코드에서 호출하는 URL추출
#         url = open_popup_js.split("'")[1]
#         print(f'\n\n 확인을 위한 출력 url :   {url}')
        
#         #새창에서 보여줄 내용을 POST로 요청
#         yield scrapy.FormRequest(
#             url,
#             method ='POST',
#             formdata={
#                 'mktTpCd': 'ALL',
#                 'searchText': '',
#                 'currentPage': '1',
#                 'pageSize': '5000'
#             },
#             callback = self.parse_table
#         )
    
#     def parse_table(self,response):
#         #페이지내 table태그를 추출하여 pandas DataFrame으로 읽기
#         dfs = pd.read_html(response.text)
#         df = dfs[0]
#         #필요 컬럼만 선택하여 item으로 저장 및 반환      
#         for row in df.itertuples():
#             item = CrawlstockinfoItem()
#             item['회사명'] = row[2]
#             item['종목코드'] = row[3]
#             item['업종'] = row[4]
#             item['주요제품'] = row[5]
#             item['상장일'] = row[6]
#             item['결산월'] = row[7]
#             item['대표자명'] = row[8]
#             item['홈페이지'] = row[9]
#             item['지역'] = row[10]
#             print('#'*20)
#             print('회사명:  ', item['회사명'])
#             print('종목코드:  ', item['종목코드'])
#             print('업종:  ', item['업종'])            
#             print('#'*20)
#             yield item
            
        
        
        
         
        
    