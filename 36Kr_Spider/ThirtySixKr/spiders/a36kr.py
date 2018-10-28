# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
import math
from ThirtySixKr.items import ThirtysixkrItem
from scrapy.http import Request


class A36krSpider(scrapy.Spider):
    name = "36kr"
    allowed_domains = [
        "36kr.com",
        "pic.36krcnd.com"
    ]
    start_urls = [
        'https://36kr.com/api/search-column/mainsite?'
    ]
    
    #获取帖子总数，生成分页URL
    def parse(self, response):
        jsonData = json.loads(response.body.decode('utf-8'))
        total_count = int(jsonData['data']['total_count'])
        page_count = math.ceil(total_count / 20) #计算共有多少分页
        print(total_count, page_count)
        for i in range(page_count):
            time.sleep(1)
            nextPage_url = 'https://36kr.com/api/search-column/mainsite?per_page=20&page=' + str(i+1)
            yield scrapy.Request(nextPage_url, callback=self.parse_title)
            
    #提取标题
    def parse_title(self, response):
        html = response.body.decode('utf-8')
        jsonData = json.loads(re.sub('<em class=\'highlight\'>|</em>|&nbsp', '', html))
        itemData = jsonData["data"]["items"]
        for each in itemData:
            item = ThirtysixkrItem()
            item['platform'] = '36Kr'
            article_url = 'http://36kr.com/api/post/' + str(each['id']) + '/next'
            item['url'] = article_url
            item['cover_img'] = each['cover']
            item['title'] = each['title']
            item['time'] = each['published_at']
            item['tags'] = each['extraction_tags']
            item['summary'] = each['summary']
            item['column_name'] = each['column_name']
            yield scrapy.Request(article_url, dont_filter=True, meta={'item': item}, callback=self.parse_content)

    #提取内容
    def parse_content(self, response):
        time.sleep(0.5)
        item = response.meta['item']
        html = response.body.decode('utf-8')
        # print("length:" + str(len(html)))
        jsonData = json.loads(html)
        contentData = jsonData["data"]["content"]
        contentText = re.sub('<.*?>', '', contentData)
        item['content'] = contentText
        yield item
