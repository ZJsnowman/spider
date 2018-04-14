# -*- coding: utf-8 -*-
import scrapy


class Zhihu2Spider(scrapy.Spider):
    name = 'zhihu2'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass
