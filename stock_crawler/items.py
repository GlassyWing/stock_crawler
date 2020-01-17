# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    quotes = Field()
    size = Field()


class MainTargetItem(scrapy.Item):
    targets = Field()
    size = Field()


class CompanyItem(scrapy.Item):
    code = Field()
    name = Field()
    intro = Field()
    manage = Field()
    ssrq = Field()
    clrq = Field()
    fxl = Field()
    fxfy = Field()
    mgfxj = Field()
    fxzsz = Field()
    srkpj = Field()
    srspj = Field()
    srhsl = Field()
    srzgj = Field()
    djzql = Field()
    wxpszql = Field()
    mjzjje = Field()
    zczb = Field()
