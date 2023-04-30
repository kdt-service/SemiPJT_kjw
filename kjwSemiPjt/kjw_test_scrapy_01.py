import scrapy


class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage']

    def parse(self, response):
        for tr in response.xpath('//*[@id="content"]/div[2]/div[1]/div/table/tbody/tr'):
            company_name = tr.xpath('./td[2]/a/text()').get()
            company_code = tr.xpath('./td[1]/a/text()').get()
            yield {'company_name': company_name, 'company_code': company_code}
