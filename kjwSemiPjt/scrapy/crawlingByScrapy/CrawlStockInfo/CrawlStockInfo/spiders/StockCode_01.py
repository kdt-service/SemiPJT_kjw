import requests
import pandas as pd
import scrapy
import os
import csv
from CrawlStockInfo.items import CrawlstockinfoItem

class StockCodeSpider(scrapy.Spider):
    name = 'stockcode_01'
    start_urls = ['https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage']
    
    def parse(self, response):
        #엑셀 다운로드 링크 추출
        onclick_value = response.css('a.xls-btn::attr(onclick)').get()
        print(f'\n\n첫번째 시도한 onclick_value: {onclick_value}\n\n')
        #url = 'https://kind.krx.co.kr/common/downloadExcel.do?name=download&url={}'.format(onclick_value.split("'")[1])
        #td = response.css('td')
        #onclick_value = td.css('a::attr(onclick)').get()
        #print(f'#################### onclick_value:  {onclick_value}')
        if onclick_value:
            split_value = onclick_value.split("'")
            print(f'\n\n split_value입니다.  {split_value} \n\n')
            print(f'\n\n split_value의 크기는  {len(split_value)}\n\n')
            if len(split_value) > 1:
                print(f'\n\n onclick_value시작하면서 url에 할당하기 바로 직전입니다. \n\n')
                url = 'https://kind.krx.co.kr/common/downloadExcel.do?name=download&url={}'.format(onclick_value.split("'")[1])
                print(f'\n\n url이 무엇이냐?  {url} \n\n')
                #엑셀파일 다운로드
                r = requests.get(url, allow_redirects=True)
                file_path_01 = os.path.join(os.getcwd(), 'FileHouseStock', 'stockcode_001.xls')
                open(file_path_01, 'wb').write(r.content)
                #csv파일로 변환                  
                    #엑셀파일도 pandas의 read_excel()함수를 통해 데이터프레임 만들 수 있지만, 
                    #CSV파일이 엑셀파일보다 용량이 작아서 빠르고 효율적이다.
                df = pd.read_excel(file_path_01, engine='xlrd')
                file_path_02 = os.path.join(os.getcwd(), 'CrawlStockInfo\\FileHouseStock', 'stockcode_001_csv')
                df.to_csv(file_path_02, index=False)
                #csv파일만 읽어서 추출
                with open(file_path_02, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    td = response.css('td')
                    onclick_value = td.css('a::attr(onclick)').get()
                    print(f'\n with open문에서 시도한 onclick_value: {onclick_value} \n')
                    for row in reader:
                        item = CrawlstockinfoItem()
                        item['회사명'] = row['회사명']
                        item['종목코드'] = row['종목코드']
                        item['업종'] = row['업종']
                        item['주요제품'] = row['주요제품']
                        item['상장일'] = row['상장일']
                        item['결산월'] = row['결산월']
                        item['대표자명'] = row['대표자명']
                        item['홈페이지'] = row['홈페이지']
                        item['지역'] = row['지역']
                        print('#'*20)
                        print('회사명:  ', item['회사명'])
                        print('종목코드:  ', item['종목코드'])
                        print('업종:  ', item['업종'])            
                        print('#'*20)
                        yield item
                    else:
                        print(f'############### onclick_value ERROR입니다.:  {onclick_value}')
                
                    
            
        
        
        
         
        
    