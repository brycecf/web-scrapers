# -*- coding: utf-8 -*-
import itertools
import pycountry
import scrapy


class UnrocaSpider(scrapy.Spider):
    name = 'unroca'
    allowed_domains = ['unroca.org']

    country_names = [country.official_name if hasattr(country, 'official_name')
                     else country.name for country in list(pycountry.countries)]
    country_names = [name.lower().replace(' ', '-') for name in country_names]

    #base_url = 'https://www.unroca.org/{}/report/{}/'
    #url_param_tuples = list(itertools.product(country_names, range(2010, 2017)))
    #start_urls = [base_url.format(param_tuple[0], param_tuple[1]) for param_tuple in url_param_tuples]
    start_url = 'https://www.unroca.org/united-states/report/2016/'

    def parse(self, response):
        if response.status == 200:
            from scrapy.shell import inspect_response
            inspect_response(response, self)
