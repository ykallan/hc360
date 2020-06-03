# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Hc360Item(scrapy.Item):

    mobile = scrapy.Field()
    tele = scrapy.Field()
    cont_person = scrapy.Field()
    com_name = scrapy.Field()
