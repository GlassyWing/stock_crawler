# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import numpy as np
from scrapy.exceptions import DropItem

from stock_crawler.db_utils import DBUtils


class QuotesPipeline(object):
    """检查数据合法性"""

    def is_valid(self, quote):
        num_null = 0
        for ele in quote:
            num_null += 1 if ele is None else 0
        return num_null / len(quote) < .25

    def process_item(self, item, spider):
        quotes = item['quotes']

        if len(quotes) == 0:
            raise DropItem("Not any quotes found.")

        indices = np.random.choice(len(quotes), 3)

        num_valid = len(indices)
        for indice in indices:
            quote = quotes[indice]
            if not self.is_valid(quote):
                num_valid -= 1

        if num_valid / len(indices) < 0.66:
            raise DropItem("Quote data seems like not ready.")

        return item


class CompaniesPipeline(object):
    """除掉单位"""

    def process_item(self, item, spider):

        if item['srkpj'] == '--' \
                or item['srspj'] == '--' \
                or item['srhsl'] == '--' \
                or item['srzgj'] == '--':
            raise DropItem("Company data seems like not ready.")

        new_iem = {}
        new_iem.update(item)

        for key, value in item.items():
            if value == '--':
                new_iem[key] = None
            else:
                if key == 'fxl' \
                        or key == 'fxfy' \
                        or key == 'fxzsz' \
                        or key == 'mjzjje' \
                        or key == 'wxpszql' \
                        or key == 'djzql' \
                        or key == 'zczb':

                    if value[-1] == '亿':
                        new_iem[key] = float(value[:-1]) * 1e8
                    elif value[-1] == '万':
                        new_iem[key] = float(value[:-1]) * 1e4
                    elif value[-1] == '千':
                        new_iem[key] = float(value[:-1]) * 1e3
                    else:
                        new_iem[key] = float(value[:-1])
                elif key == 'djzql' or key == 'srhsl' or key == 'wxpszql':
                    new_iem[key] = float(value[:-1].replace(',', '')) / 100.
                else:
                    if key != 'code':
                        try:
                            new_iem[key] = float(value)
                        except Exception:
                            pass

        return new_iem


class CompaniesPostgresPipeline(object):
    """保存公司信息至postgres数据库"""

    def __init__(self, database_config):
        self.database_config = database_config

    def process_item(self, item, spider):
        self.db_utils.upsert_company(item)
        return item

    def open_spider(self, spider):
        self.db_utils = DBUtils.init(self.database_config)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(database_config=crawler.settings.get('POSTGRESQL_CONFIG'))


class QuotesPostgresPipeline(object):
    """保存股市行情信息至postgres数据库"""

    def __init__(self, database_config):
        self.database_config = database_config

    def process_item(self, item, spider):
        quotes = item['quotes']
        self.db_utils.upsert_quotes(quotes)

        return item

    def open_spider(self, spider):
        self.db_utils = DBUtils.init(self.database_config)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(database_config=crawler.settings.get('POSTGRESQL_CONFIG'))
