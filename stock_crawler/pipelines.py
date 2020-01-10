# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import numpy as np
import psycopg2.errors as errors
from psycopg2.pool import ThreadedConnectionPool
from scrapy.exceptions import DropItem


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


class PostgresPipeline(object):
    """保存至postgres数据库"""
    UPSERT_SQL = f"""
        INSERT INTO quotes (NAME, CODE, OPENING_PRICE, LATEST_PRICE, QUOTE_CHANGE,
        CHANGE, VOLUME, TURNOVER, AMPLITUDE, TURNOVER_RATE, "PE_ratio", VOLUME_RATIO,
        MAX_PRICE, MIN_PRICE, CLOSING_PRICE, "PB_ratio", MARKET, TIME)
        VALUES 
        ({','.join(['%s'] * 18)})
        ON CONFLICT ON CONSTRAINT quotes_pkey
        DO UPDATE SET latest_price = excluded.latest_price,
                      change = excluded.change,
                      volume = excluded.volume,
                      turnover = excluded.turnover,
                      amplitude = excluded.amplitude,
                      turnover_rate = excluded.turnover_rate,
                      volume_ratio = excluded.volume_ratio,
                      max_price = excluded.max_price,
                      min_price = excluded.min_price
    """

    def __init__(self, database_config):
        self.database_config = database_config

    def process_item(self, item, spider):
        quotes = item['quotes']

        conn = self.conn_pool.getconn()
        try:
            with conn.cursor() as cur:
                try:
                    cur.executemany(PostgresPipeline.UPSERT_SQL, quotes)
                    conn.commit()
                except errors.UniqueViolation as e:
                    print("当前记录已存在")
                except errors.NotNullViolation as e:
                    print("违反非空约束")
        finally:
            self.conn_pool.putconn(conn)

        return item

    def open_spider(self, spider):
        pool_config = self.database_config['pool']
        conn_config = self.database_config['conn']
        self.conn_pool = ThreadedConnectionPool(minconn=pool_config['min'],
                                                maxconn=pool_config['max'],
                                                **conn_config)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(database_config=crawler.settings.get('POSTGRESQL_CONFIG'))

    def close_spider(self, spider):
        self.conn_pool.closeall()
