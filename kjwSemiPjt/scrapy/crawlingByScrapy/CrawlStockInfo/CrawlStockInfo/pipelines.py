# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import os
from scrapy.exporters import CsvItemExporter
from itemadapter import ItemAdapter
import datetime

class CrawlstockinfoPipeline:
    def __init__(self):
        time_stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name=f'stockinfo_{time_stamp}.csv'
        file_path = os.path.join(os.getcwd(), 'FileHouseStock', file_name)
        self.file = open(file_path, 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

