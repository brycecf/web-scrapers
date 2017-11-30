# -*- coding: utf-8 -*-
from arms_transfers.items import ArmsTransferItem
from bs4 import BeautifulSoup
import itertools
import pycountry
import scrapy


class UnrocaSpider(scrapy.Spider):
    name = 'unroca'
    allowed_domains = ['unroca.org']

    @staticmethod
    def get_country_names():
        for country in list(pycountry.countries):
            yield country.name.lower().replace(' ', '-')
            if hasattr(country, 'official_name'):
                yield country.official_name.lower().replace(' ', '-')

    def start_requests(self):
        country_names = set(UnrocaSpider.get_country_names())
        base_url = 'https://www.unroca.org/{}/report/{}/'
        url_param_tuples = list(itertools.product(country_names, range(2010, 2017)))
        start_urls = [base_url.format(param_tuple[0], param_tuple[1]) for param_tuple in url_param_tuples]
        for url in start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        if response.status == 200:

            # Due to random UN redirects ensure that we are looking at a state's original report.
            doc_h4 = response.selector.xpath('//h4[contains(@class, "unroca")]')
            doc_h4_text = doc_h4.xpath('./text()')
            if len(doc_h4_text) >= 1 and doc_h4_text[0].extract() == 'UNROCA original report':
                report_details = doc_h4.xpath('following-sibling::*/text()')[0].extract().split()
                reporting_year = report_details[-1]
                reporting_state = ' '.join(report_details[:-1])
                div_panels = response.selector.xpath('//div[contains(@class, "panel-body")]')
                export_trows = div_panels[1].xpath('./table/tbody/tr')
                import_trows = div_panels[2].xpath('./table/tbody/tr')

                for row in export_trows:
                    export_item = ArmsTransferItem()

                    row_soup = BeautifulSoup(row.extract(), 'html.parser')
                    row_data = row_soup.find_all('td')

                    export_item['year'] = reporting_year
                    export_item['exporter'] = reporting_state
                    export_item['importer'] = row_data[0].text.strip()
                    export_item['category'] = row_soup.find('th').text.strip()
                    export_item['num_items'] = row_data[1].text.strip()
                    export_item['state_of_origin'] = row_data[2].text.strip()
                    export_item['intermediate_locations'] = row_data[3].text.strip()
                    export_item['comments'] = row_data[4].text.strip()

                    yield export_item

                for row in import_trows:
                    import_item = ArmsTransferItem()

                    row_soup = BeautifulSoup(row.extract(), 'html.parser')
                    row_data = row_soup.find_all('td')

                    import_item['year'] = reporting_year
                    import_item['exporter'] = row_data[0].text.strip()
                    import_item['importer'] = reporting_state
                    import_item['category'] = row_soup.find('th').text.strip()
                    import_item['num_items'] = row_data[1].text.strip()
                    import_item['state_of_origin'] = row_data[2].text.strip()
                    import_item['intermediate_locations'] = row_data[3].text.strip()
                    import_item['comments'] = row_data[4].text.strip()

                    yield import_item