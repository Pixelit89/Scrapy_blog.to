# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TorontoRestItem(scrapy.Item):
    # define the fields for your item here like:
    business_name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    location = scrapy.Field()
    category = scrapy.Field()
    type = scrapy.Field()