# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os
from scrapy.exporters import CsvItemExporter
from itemadapter import ItemAdapter


class KjwtutorialPipeline(object):
    def __init__(self):
        #self.file = open('KjwTutorial/FileHouse/movies_3.csv', 'wb')
        #self.file = open('FileHouse/movies_4.csv', 'wb')
        #os.chdir('D:\\MultiCampus\\semi_pjt_kjw\\kjwSemiPjt\\scrapy\\tutorial\\KjwTutorial\\KjwTutorial')
        #os.chdir('D:/MultiCampus/semi_pjt_kjw/kjwSemiPjt/scrapy/tutorial/KjwTutorial/KjwTutorial')
        # 디렉토리 구분은 \\ 혹은 / 으로 해야 된다.
        #currentDir = os.getcwd()
        #print(f'지금디렉토리는 {currentDir}입니다. ')
        #os.chdir(os.getcwd())
        #위 코딩에서 os.getcwd() 즉 CurrentDir은 \\ 혹은 / 으로 구분된 디렉토리가 아니고 \ 으로 구분되어 있어서 notFoundDirectoryErro가 발생한다.
        #print()해보면 os.getcwd()가 D:\MultiCampus\semi_pjt_kjw\kjwSemiPjt\scrapy\tutorial\KjwTutorial\KjwTutorial 로서 \ 하나다.. 안된다. \\ 두개로 구분되어야 한다.
        #file_path = os.path.join('FileHouse', 'movie_9.csv')
        #file_path = 'FileHouse/movie_10.csv'
        file_path = os.path.join(os.getcwd(), 'KjwTutorial\\FileHouse','movie_15.csv')
        self.file = open(file_path, 'wb')
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
