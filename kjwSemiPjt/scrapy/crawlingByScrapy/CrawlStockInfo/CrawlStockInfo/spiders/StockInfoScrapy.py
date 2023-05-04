import requests
import pandas as pd
import scrapy
import os
import csv
import io
import re
import glob
from CrawlStockInfo.items import CrawlstockinfoItem
from bs4 import BeautifulSoup

class StockCodeSpider(scrapy.Spider):
    name = "stockinfo"
    
    def start_requests(self):
        file_path = os.path.join(os.getcwd(), 'FileHouseStock')
        file_list = glob.glob(os.path.join(file_path, 'stockcode_*.csv'))
        file_latest = max(file_list, key= os.path.getctime)
        stock_codes = pd.read_csv(file_latest)
        #file_path = os.path.join(os.getcwd(),'FileHouseStock', 'stockcodeTest.csv')
        #stock_codes = pd.read_csv(file_path)
        stock_codes['종목코드'] = stock_codes['종목코드'].str.strip('"')
        for code in stock_codes['종목코드']:
            url = f'https://finance.naver.com/item/coinfo.naver?code={code}'
            yield scrapy.Request(url=url, callback=self.parse, meta={'code': code})
    
    def parse(self, response):
        print(f'\n\n확인용출력:\n\n{response.text[:1000]}\n\n')
        item = CrawlstockinfoItem()
        code = response.meta['code']
        item['종목명'] = response.css('#middle > div.h_company > div.wrap_company > h2 > a::text').get()
        item['종목코드'] = code
        item['종목코드'] = '"'+item['종목코드']+'"'
        item['시장구분'] = response.css('#middle > div.h_company > div.wrap_company > div> img::attr(alt)').get()
        item['업종구분'] = response.css('#pArea > div.wrapper-table >dt:nth-child(3)::text').get()
        item['투자의견'] = response.xpath('//*[@id="cTB15"]/tbody/tr[2]/td[1]/b/text()').get()
        item['현재가'] = response.css('#chart_area > div.rate_info > div > p.no_today > em > span.blind::text').get()
        item['매출액'] = response.css('#bG05RlB6cn > .gHead01 all-width > tbody > tr:nth-child(1) > td:nth-child(3) > span.blind::text').get()
        item['순이익'] = response.css('#tab_con1 > div:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(2)::text').get()
        item['순이익율'] = response.css('#tab_con1 > div:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(4)::text').get()
        item['PER'] = response.css('#tab_con1 > div:nth-child(6) > table > tbody > tr:nth-child(3) > td em::text').get()
        item['PBR'] = response.css('#tab_con1 > div:nth-child(6) > table > tbody > tr:nth-child(5) > td em::text').get()
        item['ROE'] = response.css('#tab_con1 > div:nth-child(6) > table > tbody > tr:nth-child(9) > td em::text').get()
        item['배당수익율'] = response.css('#tab_con1 > div:nth-child(6) > table > tbody > tr:nth-child(11) > td em::text').get()
        item['부채비율'] = response.css('#tab_con1 > div:nth-child(4) > table > tbody > tr:nth-child(2) > td:nth-child(2)::text').get()
        
        print('#'*20)
        print('종목명:  ', item['종목명'])
        print('종목코드:  ', item['종목코드'])
        print('업종구분:  ', item['업종구분'])            
        print('#'*20)
        yield item

        # img_tag = response.css('#pointerBG >img')
        # if img_tag:
        #     item['투자의견'] = response.css('#pointerBG >img::attr(alt)').get().split(':')[-1].strip()
        # else:
        #     item['투자의견'] = ''    
        #item['투자의견'] = response.css('#cTB15 > tbody > tr:nth-child(2) > td.noline-bottom.line-right.center.cUp > b::text').get()
        #item['투자의견'] = response.css('#cTB15 > tbody > tr:nth-child(2) > td.noline-bottom.line-right.center.cUp > b::text').get()
                #item['투자의견'] = item['투자의견'][0] if item['투자의견'] else ''                                    
                        #item['매출액'] = response.css('#tab_con1 > div:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2)::text').get()