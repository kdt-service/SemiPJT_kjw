# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KjwtutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    title = scrapy.Field()
    content = scrapy.Field()
    grade = scrapy.Field()
    date_show = scrapy.Field()
    rate = scrapy.Field()
    #pass