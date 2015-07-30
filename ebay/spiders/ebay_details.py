# -*- coding: utf-8 -*-
import scrapy
from ebay.items import DetailsItem
import re
import lxml
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
import unicodedata


class EbayDetailsSpider(scrapy.Spider):
    name = "ebay_details"
    allowed_domains = ["ebay.com", "ebaydesc.com"]
    start_urls = (
        line.strip() for line in open("ebay_items.txt", "r")
    )
    
    def parseDetails(self, response):
      iframe_url = response.xpath('//*[@id="desc_ifr"]').xpath("@src").extract()[0]        
      yield scrapy.Request(iframe_url, callback=self.parseIframe)

    def parseIframe(self, response):
        item = DetailsItem()
        item['description'] = response.extract()
        yield item
 
    def parseIframe1(self, response):
        item = response.meta['item']      
        self.logger.info('debug url %s', response.url)
        self.logger.info('debug item %s', ",".join(item))
        if item:
          item['description'] = "I am description"        
          self.logger.info("I am item %s", item.join(","))
        else:
          inspect_response(response, self)
        
        yield scrapy.Request(response.meta['parent_url'], callback=self.parseDetail, meta={ "item": item })


    def parse(self, response):
        item = DetailsItem()
        itemSpecifics = list()
        attributes = response.css("div.itemAttr").css('table td')
        iframe_url = response.xpath('//*[@id="desc_ifr"]').xpath("@src").extract()[0]
         
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

                
            if 'value' in locals() and 'key' in locals():
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
        req = scrapy.Request(iframe_url, callback=self.parse_iframe, meta={ "item":item })
        yield req
         
    def parse_iframe(self, response):
       item = response.meta['item']
       html = response.xpath("//*").extract()[0]
       
       cleaner = Cleaner()
       cleaner.javascript = True
       cleaner.style = True
       html = unicodedata.normalize("NFKD", html).encode('ascii','ignore')
       clean = cleaner.clean_html(html) 
       

       soup = BeautifulSoup(clean, 'lxml')
       text = soup.get_text()

       
       item['description'] = text
       yield item
    
        
        
