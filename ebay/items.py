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
    description   = scrapy.Field()
    price         = scrapy.Field()
    category      = scrapy.Field()
    asin          = scrapy.Field()
    sold          = scrapy.Field()
    sold_items    = scrapy.Field()
    
class SoldItem(scrapy.Item):
    ebayID  = scrapy.Field()
    price   = scrapy.Field()
    quantity = scrapy.Field()
    date     = scrapy.Field()
    
class AmazonItem(scrapy.Item):
    title = scrapy.Field()
    reviews = scrapy.Field()
    soldBy  = scrapy.Field()
    isFBA   = scrapy.Field()
    price   = scrapy.Field()
    availability = scrapy.Field()
    isInStock = scrapy.Field()
    shortDesc = scrapy.Field()
    longDesc  = scrapy.Field()
    longDescRaw = scrapy.Field()
    asin      = scrapy.Field()
    upc       = scrapy.Field()
    ean       = scrapy.Field()
    mpn       = scrapy.Field()
    dimensions = scrapy.Field()
    reviewsNum = scrapy.Field()
    sellerRank = scrapy.Field()
    images_url = scrapy.Field()
    images = scrapy.Field()
    