"""
股市行情
"""
import json
import numpy as np
from urllib.parse import urlencode

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import DropItem

from stock_crawler.items import QuoteItem

from datetime import datetime, time, timedelta

quotes_api = "http://90.push2.eastmoney.com/api/qt/clist/get"

# 行情查询参数
quotes_kw = {
    'po': 1,  # unknown
    'pn': 1,  # 页号
    'np': 1,  # 多少页
    'pz': 1,  # 每页大小
    'fltt': 2,  # 精度
    'invt': 2,
    'fid': 'f3',  # 排序字段
    'fields': 'f14,f12,f17,f2,f3,f4,f5,f6,f7,f8,f9,f10,f15,f16,f18,f23',  # 查询域
    'fs': 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23',  # 某种股市坐标
    'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
}

# 各板对应参数
sock_part_dict = {
    '泸深A股': 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23',
    '上证A股': 'm:1 t:2,m:1 t:23',
    '深证A股': 'm:0 t:6,m:0 t:13,m:0 t:80',
    '新股': 'm:0 f:8,m:1 f:8',
    '中小板': 'm:0 t:13',
    '创业板': 'm:0 t:80',
    '科创板': 'm:1 t:23',
    '泸股通': 'b:BK0707',
    '深股通': 'b:BK0804',
    'B股': 'm:0 t:7,m:1 t:3'
}

# 每个域所代表的值
fields_dict = {
    'f2': '最新价',
    'f3': '涨跌幅',
    'f4': '涨跌额',
    'f5': '成交量',
    'f6': '成交额',
    'f7': '振幅',
    'f8': '换手率',
    'f9': '市盈率',
    'f10': '量比',
    'f12': '代码',
    'f14': '名称',
    'f15': '最高',
    'f16': '最低',
    'f17': '今开',
    'f18': '昨收',
    'f23': '市净率',
}

fields_en_dict = {
    'f2': 'latest_price',
    'f3': 'quote_change',
    'f4': 'change',
    'f5': 'volume',
    'f6': 'turnover',
    'f7': 'amplitude',
    'f8': 'turnover_rate',
    'f9': 'PE_ratio',
    'f10': 'volume_ratio',
    'f12': 'code',
    'f14': 'name',
    'f15': 'max_price',
    'f16': 'min_price',
    'f17': 'opening_price',
    'f18': 'closing_price',
    'f23': 'PB_ratio'
}

column2field = {
    'name': 'f14',
    'code': 'f12',
    'opening_price': 'f17',
    'latest_price': 'f2',
    'quote_change': 'f3',
    'change': 'f4',
    'volume': 'f5',
    'turnover': 'f6',
    'amplitude': 'f7',
    'turnover_rate': 'f8',
    'PE_ratio': 'f9',
    'volume_ratio': 'f10',
    'max_price': 'f15',
    'min_price': 'f16',
    'closing_price': 'f18',
    'PB_ratio': 'f23'
}

columns = ['name', 'code', 'opening_price', 'latest_price', 'quote_change',
           'change', 'volume', 'turnover', 'amplitude', 'turnover_rate', 'PE_ratio',
           'volume_ratio', 'max_price', 'min_price', 'closing_price', 'PB_ratio']
fields = ['f14', 'f12', 'f17', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10',
          'f15', 'f16', 'f18', 'f23']


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        for fs_k, fs_v in sock_part_dict.items():
            params = {}
            params.update(quotes_kw)
            params.update({"fs": fs_v})

            url = quotes_api + "?" + urlencode(params)
            req = Request(method='GET', url=url, callback=self.parse_plate)
            req.meta['fs_k'] = fs_k
            req.meta['fs_v'] = fs_v
            yield req
            # break

    def parse_plate(self, response):
        """获取每个板的元数据"""
        fs_v = response.meta['fs_v']
        fs_k = response.meta['fs_k']

        result = json.loads(response.body, encoding='utf-8')['data']
        self.logger.info(f"获取`{fs_k}`行情，共{result['total']}条")

        total = result['total']  # 总记录
        pz = self.settings.get('PAGE_SIZE')  # 每页大小

        num_page = total // pz
        remain = total - num_page * pz

        if remain < 0:
            raise DropItem(f"Fail to download data from `{fs_k}`")

        if remain > 0:
            num_page += 1

        for pn in range(1, num_page + 1):
            param = {}
            param.update(quotes_kw)
            param.update({
                'pn': pn,
                'pz': pz,
                'fs': fs_v
            })

            url = quotes_api + "?" + urlencode(param)
            req = Request(method='GET', url=url, callback=self.parse_page)
            req.meta['pn'] = pn
            req.meta['fs_k'] = fs_k
            req.meta['num_page'] = num_page

            yield req

    def _hit_time(self):
        """最新的记录只更新到最近的记录时间点"""

        now_time = datetime.now()
        year = now_time.year
        month = now_time.month
        day = now_time.day
        hour = now_time.hour

        now_minute = now_time.minute / 60.

        # 每半小时为一个记录时间点
        minute_series = np.array([0, 0.5, 1])

        min_ind = np.argmin(np.abs(now_minute - minute_series))

        minute = int(minute_series[min_ind] * 60)
        if minute == 60:
            now_time = now_time + timedelta(hour + 1)
            hour = now_time.hour
            minute = 0

        return datetime(year=year,
                        month=month,
                        day=day,
                        hour=hour,
                        minute=minute)

    def _map_to_value(self, data):
        """获得指定域的值"""
        value = []
        for field in fields:
            if data[field] == '-':
                value.append(None)
            else:
                value.append(data[field])
        return value

    def parse_page(self, response):
        """获取某个股市板中一页的数据"""
        pn = response.meta['pn']
        fs_k = response.meta['fs_k']
        num_page = response.meta['num_page']
        self.logger.info(f'获取`{fs_k}`中第{pn}页数据，共{num_page}页。')

        result = json.loads(response.body, encoding='utf-8')['data']['diff']

        values = []
        for data in result:
            value = self._map_to_value(data)
            value.append(fs_k)
            value.append(self._hit_time())

            values.append(value)

        item = QuoteItem()
        item['size'] = len(values)
        item['quotes'] = values

        yield item


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(QuotesSpider, name="quotes_spider")
    process.start()
