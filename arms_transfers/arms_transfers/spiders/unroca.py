# -*- coding: utf-8 -*-
from arms_transfers.items import ArmsTransferItem
import itertools
import pycountry
import scrapy
import urllib3


class UnrocaSpider(scrapy.Spider):
    name = 'unroca'
    allowed_domains = ['unroca.org']

    country_names = [country.official_name if hasattr(country, 'official_name')
                     else country.name for country in list(pycountry.countries)]
    country_names = [name.lower().replace(' ', '-') for name in country_names]

    base_url = 'https://www.unroca.org/{}/report/{}/'
    url_param_tuples = list(itertools.product(country_names, range(2010, 2017)))
    start_urls = [base_url.format(param_tuple[0], param_tuple[1]) for param_tuple in url_param_tuples]

    def parse(self, response):
        if response.status == 200:
            url_params = urllib3.util.parse_url(response.request.url).path.split('/')
            div_panels = response.selector.xpath('//div[contains(@class, "panel-body")]')
            export_trows = div_panels[1].xpath('./table/tbody/tr')
            import_trows = div_panels[2].xpath('./table/tbody/tr')

            for row in export_trows:
                export_item = ArmsTransferItem()

                arms_transfer_values = list(map(str.strip, row.xpath('./td/text()').extract()))

                export_item['year'] = url_params[3]
                export_item['exporter'] = url_params[1]
                export_item['importer'] = arms_transfer_values[0]
                export_item['category'] = row.xpath('./th/text()')[0].extract()
                export_item['num_items'] = arms_transfer_values[1]
                export_item['state_of_origin'] =arms_transfer_values[2]
                export_item['intermediate_locations'] = None
                export_item['comments'] = arms_transfer_values[3]

                yield export_item

            for row in import_trows:
                import_item = ArmsTransferItem()

                arms_transfer_values = list(map(str.strip, row.xpath('./td/text()').extract()))

                import_item['year'] = url_params[3]
                import_item['exporter'] = arms_transfer_values[0]
                import_item['importer'] = url_params[1]
                import_item['category'] = row.xpath('./th/text()')[0].extract()
                import_item['num_items'] = arms_transfer_values[1]
                import_item['state_of_origin'] = arms_transfer_values[2]
                import_item['intermediate_locations'] = None
                import_item['comments'] = arms_transfer_values[3]

                yield import_item