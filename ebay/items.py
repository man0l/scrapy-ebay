# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EbayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    sold = scrapy.Field()
    price = scrapy.Field()
    country = scrapy.Field()
    image = scrapy.Field()
    
class DetailsItem(scrapy.Item):
    ebayID        = scrapy.Field()
    upc           = scrapy.Field()
    mpn           = scrapy.Field()
    brand         = scrapy.Field()
    ean           = scrapy.Field()
    url           = scrapy.Field()    
    