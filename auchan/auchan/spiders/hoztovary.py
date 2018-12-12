# -*- coding: utf-8 -*-
import scrapy


class HoztovarySpider(scrapy.Spider):
    name = 'hoztovary'
    allowed_domains = ['auchan.ru']
    start_urls = ['http://auchan.ru/']

    def parse(self, response):
        pass
