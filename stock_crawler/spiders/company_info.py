"""
公司信息
"""
import json
from time import sleep

import pandas as pd
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

from stock_crawler.items import CompanyItem

company_info_api = 'http://f10.eastmoney.com/CompanySurvey/CompanySurveyAjax?code={code}'

fields_dict = {
    'jyfw': '经营范围',
    'gsjj': '公司简介',
    'clrq': '成立日期',
    'ssrq': '上市日期'
}


class CompanyInfoSpider(scrapy.Spider):
    name = "company_inf"

    custom_settings = {
        'ITEM_PIPELINES': {
            'stock_crawler.pipelines.CompaniesPipeline': 300,
            'stock_crawler.pipelines.CompaniesPostgresPipeline': 301,
        }
    }

    def parse(self, response):
        data = json.loads(response.body, encoding='utf-8')
        jbzl = data['jbzl']
        fxxg = data['fxxg']

        item = CompanyItem()
        item['code'] = jbzl['agdm']
        item['name'] = jbzl['gsmc']
        item['intro'] = jbzl['gsjj'].strip()
        item['manage'] = jbzl['jyfw'].strip()
        item['zczb'] = jbzl['zczb']

        item['ssrq'] = fxxg['ssrq']
        item['clrq'] = fxxg['clrq']
        item['fxl'] = fxxg['fxl']
        item['fxfy'] = fxxg['fxfy']
        item['fxzsz'] = fxxg['fxzsz']
        item['srkpj'] = fxxg['srkpj']
        item['srspj'] = fxxg['srspj']
        item['srhsl'] = fxxg['srhsl']
        item['srzgj'] = fxxg['srzgj']
        item['wxpszql'] = fxxg['wxpszql']
        item['djzql'] = fxxg['djzql']
        item['mjzjje'] = fxxg['mjzjje']
        item['mgfxj'] = fxxg['mgfxj']

        return item

    def __init__(self, companies, **kwargs):
        super().__init__(**kwargs)

        self.companies = companies

    def start_requests(self):
        for company_code in self.companies:
            # 上海
            if company_code.startswith('6'):
                company_code = 'SH' + company_code
            # 深圳
            else:
                company_code = 'SZ' + company_code
            yield Request(company_info_api.format(code=company_code))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        with open(crawler.settings['COMPANY_CODES_INDEX'], 'r') as file:
            codes = file.readlines()
        print(codes)
        return cls(companies=codes)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(CompanyInfoSpider, name="company_inf", companies=['002613'])
    process.start()
    sleep(3)
