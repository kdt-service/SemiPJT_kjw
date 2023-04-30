from pathlib import Path

import scrapy

import re

from KjwTutorial.items import KjwtutorialItem
#from items import KjwtutorialItem

class MovieSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        urls = [
            'https://movie.daum.net/ranking/reservation'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # response.css() 혹은 response.xpath() 메서드로 원하는 정보를 가져올 수 있다.
        # 위의 둘 중에서 본인이 편한 메서드를 사용하면 된다.
        # 데이터 = response.css('문법')
        movie_sels = response.css('ol.list_movieranking  li')
        for movie_sel in movie_sels:
            #item = {}
            item = KjwtutorialItem()
            item['title'] = movie_sel.css('.tit_item a::text').get()
            item['content'] = movie_sel.css('a::text').get()
            item['grade'] = movie_sel.css('span.txt_grade::text').get()
            item['date_show'] = movie_sel.css('.txt_info > span.txt_num::text').get()
            item['rate'] = movie_sel.css('span.txt_num::text').get()
            print('#'*20)
            print('제목: ', item['title'])
            print('내용: ', item['content'])
            print('평점: ', item['grade'])
            print('개봉일: ', item['date_show'])
            print('예매율: ', item['rate'])
            print('#'*20)
            print('\n\n yield item_start:')
            yield item
            print('yield item_end \n\n ')
            
            