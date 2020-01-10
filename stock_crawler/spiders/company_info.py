"""
公司信息
"""
from time import sleep

from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.selector import Selector
from scrapy import Request
import scrapy
import json

company_info_api = 'http://f10.eastmoney.com/CompanySurvey/CompanySurveyAjax?code={code}'

fields_dict = {
    'jyfw': '经营范围',
    'gsjj': '公司简介',
    'clrq': '成立日期',
    'ssrq': '上市日期'
}


class CompanyInfoSpider(scrapy.Spider):

    def parse(self, response):
        data = json.loads(response.body, encoding='utf-8')
        print(data['jbzl']['gsjj'])

    def __init__(self, name, companies, **kwargs):
        kwargs['name'] = name
        super().__init__(**kwargs)
        self.companies = companies

    def start_requests(self):
        for company_code in self.companies:
            yield Request(company_info_api.format(code=company_code))


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(CompanyInfoSpider, name="company_inf", companies=['SH688116'])
    process.start()
    sleep(3)
