# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThirtysixkrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    platform = scrapy.Field()
    url = scrapy.Field()  # 文章原始url
    cover_img = scrapy.Field()  # 文章原始封面图url
    title = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()
    summary = scrapy.Field()
    column_name = scrapy.Field()
