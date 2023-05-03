# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlstockinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    회사명 = scrapy.Field()
    종목코드 = scrapy.Field()
    업종 = scrapy.Field()
    주요제품 = scrapy.Field()
    상장일 = scrapy.Field()
    결산월 = scrapy.Field()
    대표자명 = scrapy.Field()
    홈페이지 = scrapy.Field()
    지역 = scrapy.Field()
    #pass
    pass

    

