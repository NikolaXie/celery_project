import scrapy
from scrapy.http import Request
import re
import datetime
from news_Spider.items import BaiduNewsSpiderItem
from scrapy.selector import Selector

class baiduNewsSpider(scrapy.Spider):

    name = "baiduNews"

    #搜索关键词
    keyWords = ['工业互联网', '工业大数据', '工业人工智能', '工业4.0', '智能制造', '工业云', '工业人工智能', '工业AI']

    #接受的域名范围
    allowed_domains = [
        "news.baidu.com"
    ]

    rn = 50

    start_pn = 0

    #修改时间格式（把“n小时前”改成标准时间）
    def __format_datetime(self, time_str):
        if len(time_str) < 10:
            time_str = time_str.replace('小时前', '')
            time_str = time_str.replace('分钟前', '')
            return datetime.datetime.now() - datetime.timedelta(hours=int(time_str))

        year = int(time_str[0:4])
        month = int(time_str[5:7])
        day = int(time_str[8:10])
        hour = int(time_str[12:14])
        minute = int(time_str[15:17])
        return datetime.datetime(year, month, day, hour, minute)

    #拼url
    def __set_parameter(self, key_word, start_index):
        url_tplt = "http://news.baidu.com/ns?word=title:(%s)&pn=%d&cl=2&ct=0&tn=newstitle&rn=%d&ie=utf-8&bt=0&et=0"
        return url_tplt % (key_word, start_index, self.rn)

    def start_requests(self):
        self.start_urls = list(map(lambda x: self.__set_parameter(x, self.start_pn), self.keyWords))
        requests = map(
            lambda x: Request(url=x, callback=self.parse_title),
            self.start_urls
        )
        yield from requests

    def parse_title(self, response):
        html = response.body.decode('utf-8')
        titleNodes = Selector(text=html).xpath('//h3[@class="c-title"]/a')
        infoNodes = Selector(text=html).xpath('//div[@class="c-title-author"]')
        for titleNode, infoNode in zip(titleNodes, infoNodes):
            title = ''.join(titleNode.xpath('.//text()').extract()).strip()
            url = titleNode.xpath('@href').extract_first()
            info = ''.join(infoNode.xpath('.//text()').extract())
            # print(info)

            time_strs = re.findall('([0-9]{4}年[0-9]{2}月[0-9]{2}日 [0-9]{2}:[0-9]{2})', info)
            if not time_strs:
                time_strs = re.findall('([1-9]+[0-9]*小时前|[1-9]+[0-9]*分钟前)', info)
            time = self.__format_datetime(time_strs[0])

            author = re.findall('^(.+?)\n', info)[0]

            item = BaiduNewsSpiderItem()
            item['title'] = title
            item['author'] = author
            item['time'] = time
            item['url'] = url
            yield item

        nextURL = response.xpath('.//a[@class="n"][contains(text(), "下一页>")]/@href').extract()
        if nextURL:
            nextURL = response.urljoin(nextURL[0])
            print(nextURL)
            yield Request(url=nextURL, callback=self.parse_title)
