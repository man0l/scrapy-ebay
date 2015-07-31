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
                    item['upc'] = value
                elif key == 'mpn':
                    item['mpn'] = value
                elif key == 'brand':
                    item['brand'] = value
                elif key == 'ean':
                    item['ean'] = value
        
        caregory_url =  response.xpath('//*[@id="vi-VR-brumb-lnkLst"]/table/tr[1]/td[1]/h2[1]/ul[1]/li[last()]/a[1]/@href').extract()[0]    
        #mm-saleDscPrc     
        if response.xpath('//*[@id="prcIsum"]/text()'):
           price = response.xpath('//*[@id="prcIsum"]/text()').extract()[0].replace("US $", "")
        elif response.xpath('//*[@id="saleDscPrc"]/text()'):
           price = response.xpath('//*[@id="saleDscPrc"]/text()').extract()[0].replace("US $", "")
        else:
           price = 'not_set'
        
          
            
        item['url']      = response.url
        item['ebayID']   = ebayID   
        item['price']    = price
        item['category'] = re.compile("\d+").search(caregory_url).group(0)
        req              = scrapy.Request(iframe_url, callback=self.parse_iframe, meta={ "item":item })
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
