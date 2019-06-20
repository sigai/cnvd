# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnvdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    click = scrapy.Field()
    rank = scrapy.Field()
    comment = scrapy.Field()
    follow = scrapy.Field()
    public_time = scrapy.Field()
    detail = scrapy.Field()
