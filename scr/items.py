# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category=scrapy.Field()
    url=scrapy.Field()
    name=scrapy.Field()
    site=scrapy.Field()
    email=scrapy.Field()
    phone=scrapy.Field()
    logo=scrapy.Field()
    description=scrapy.Field()
