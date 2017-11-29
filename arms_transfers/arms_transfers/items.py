# -*- coding: utf-8 -*-
import scrapy


class ArmsTransferItem(scrapy.Item):
    year = scrapy.Field()
    exporter = scrapy.Field()
    importer = scrapy.Field()
    category = scrapy.Field()
    num_items = scrapy.Field()
    state_of_origin = scrapy.Field()  # Only has a value if state_of_origin != exporter
    intermediate_locations = scrapy.Field()  # Only has a value if filled
    comments = scrapy.Field()

