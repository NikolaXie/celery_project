# -*- coding: utf-8 -*-
import scrapy


class TeSpider(scrapy.Spider):
    name = 'te'
    allowed_domains = ['emoji-cheat-sheet.com']
    start_urls = ['http://www.emoji-cheat-sheet.com/']

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)
