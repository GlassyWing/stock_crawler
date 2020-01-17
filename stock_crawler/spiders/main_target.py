"""主要指标爬虫"""
import json

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

from stock_crawler.items import MainTargetItem
from stock_crawler.utils import convert_unit

main_target_api = "http://f10.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?type=0&code={code}"

columns = ['date', 'jbmgsy', 'kfmgsy', 'xsmgsy', 'mgjzc', 'mggjj', 'mgwfply',
           'mgjyxjl', 'yyzsr', 'mlr', 'gsjlr', 'kfjlr', 'yyzsrtbzz', 'gsjlrtbzz', 'kfjlrtbzz', 'yyzsrgdhbzz',
           'gsjlrgdhbzz', 'kfjlrgdhbzz', 'jqjzcsyl', 'tbjzcsyl', 'tbzzcsyl', 'mll', 'jll', 'sjsl',
           'yskyysr', 'jyxjlyysr', 'xsxjlyysr', 'zzczzy', 'yszkzzts', 'chzzts', 'zcfzl', 'ldzczfz', 'ldbl', 'sdbl']


class MainTargetSpider(scrapy.Spider):
    name = "main_target"

    custom_settings = {
        'ITEM_PIPELINES': {
            'stock_crawler.pipelines.MainTargetsPostgresPipeline': 300,
        }
    }

    def __init__(self, companies, **kwargs):
        super().__init__(**kwargs)
        self.companies = companies

    def _map_to_value(self, code, target):
        value = [code]
        for col in columns:
            if target[col] == '-' or target[col] == '--':
                value.append(None)
            else:
                value.append(convert_unit(target[col]))
        return value

    def start_requests(self):
        for code in self.companies:

            # 上海
            if code.startswith('6'):
                company_code = 'SH' + code
            # 深圳
            else:
                company_code = 'SZ' + code
            req = Request(main_target_api.format(code=company_code))
            req.meta['code'] = code
            yield req

    def parse(self, response):
        code = response.meta['code']
        data = json.loads(response.body, encoding='utf-8')

        targets = []
        for d in data:
            targets.append(self._map_to_value(code, d))

        main_target_item = MainTargetItem()
        main_target_item['targets'] = targets
        main_target_item['size'] = len(targets)

        return main_target_item


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(MainTargetSpider, companies=['688278'])
    process.start()
