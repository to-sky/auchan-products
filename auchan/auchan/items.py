# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AuchanItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    price = scrapy.Field()
    attributes = scrapy.Field()
    sku = scrapy.Field()
    categories = scrapy.Field()
    pass
