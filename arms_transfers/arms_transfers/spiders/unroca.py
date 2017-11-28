# -*- coding: utf-8 -*-
import scrapy


class UnrocaSpider(scrapy.Spider):
    name = 'unroca'
    allowed_domains = ['unroca.org']
    start_urls = ['http://unroca.org/']

    def parse(self, response):
        pass
