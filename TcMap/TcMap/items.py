# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TcMapItem(scrapy.Item):
    # define the fields for your item here like:
    # 文件名
    fileName = scrapy.Field()
    # 行政代码
    fileCode = scrapy.Field()
    # 各地简介
    fileContent = scrapy.Field()

