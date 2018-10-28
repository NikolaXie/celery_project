# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ToutiaoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BaiduNewsSpiderItem(scrapy.Item):
    url = scrapy.Field()  # 文章原始url
    title = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()