# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os
from scrapy.exporters import CsvItemExporter
from itemadapter import ItemAdapter


class CrawlstockinfoPipeline:
    def __init__(self):
        file_path_03 = os.path.join(os.getcwd(), 'FileHouseStock', 'stockcode_new_02.csv')
        self.file = open(file_path_03, 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

