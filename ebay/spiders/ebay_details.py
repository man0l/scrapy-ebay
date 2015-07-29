# -*- coding: utf-8 -*-
import scrapy
from ebay.items import DetailsItem
import re

class EbayDetailsSpider(scrapy.Spider):
    name = "ebay_details"
    allowed_domains = ["ebay.com"]
    start_urls = (
        line.strip() for line in open("ebay_items.txt", "r")
    )

    def parse(self, response):
        item = DetailsItem()
        itemSpecifics = list()
        attributes = response.css("div.itemAttr").css('table td')
       
        match = re.compile("ebay.com/itm.*?/(\d+)").search(response.url)
        ebayID = match.group(1)
        
        for attr in attributes:
            if attr.xpath("@class"):
                key = attr.xpath('text()').extract()[0].strip().split(":")[0].lower()
                
                    
            else:    
                if attr.xpath("*[1]/*[1]"):
                   value = attr.xpath("*[1]/*[1]/text()").extract()[0].strip()
                elif attr.xpath("*[1]"):
                   value = attr.xpath("*[1]/text()").extract()[0].strip()

                
            if 'value' in locals():
                if key == 'upc':
                    item[key] = value
                elif key == 'mpn':
                    item[key] = value
                elif key == 'brand':
                    item[key] = value
                elif key == 'ean':
                    item[key] = value
                
            
            
        item['url'] = response.url
        item['ebayID'] = ebayID            
                
        return item
