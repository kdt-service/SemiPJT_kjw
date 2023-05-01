# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from scrapy.exporters import CsvItemExporter
from itemadapter import ItemAdapter


class KjwtutorialPipeline(object):
    def __init__(self):
        self.file = open('KjwTutorial/FileHouse/movies_2.csv', 'wb')
        #self.exporter = CsvItemExporter(self.file, encoding='utf-8')  
                       # encoding='utf-8'를 생략하면 encoding=None으로 처리됨
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
         
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
