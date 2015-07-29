# -*- coding: utf-8 -*-
import scrapy
import urllib
from ebay.items import EbayItem
import urlparse


class EbaySpiderSpider(scrapy.Spider):
    name = "ebay_spider"
    allowed_domains = ["ebay.com"]
    start_urls = ["http://www.ebay.com"]
	
    def parse(self, response):	
      trksid = response.css("input[type='hidden'][name='_trksid']").xpath("@value").extract()[0]       
      with open('product_names.txt') as fp:
        for name in fp:      
            yield scrapy.Request("http://www.ebay.com/sch/i.html?_from=R40&_trksid=" + trksid + "&_nkw=" + urllib.quote(name), callback=self.parse_link)
   
    def parse_link(self, response):
        for sel in response.css('ul#ListViewInner li.sresult'):
            yield scrapy.Request(sel.css("h3 a").xpath("@href").extract()[0].strip(), callback=self.parse_seller)
    
    def parse_seller(self, response):
        url = response.css("#vi-see-all-lnk").xpath("@href").extract()[0]
        url = url.strip()
        yield scrapy.Request(url, callback=self.parse_search)
     
    def parse_search(self, response):
      for sel in response.css('ul#ListViewInner li.sresult'):
        item = EbayItem()
        item['name'] = sel.css("h3 a").xpath("text()").extract()
        item['link'] = sel.css("h3 a").xpath("@href").extract()
        if sel.css(".lvprice span"):
            item['price'] = sel.css(".lvprice span").xpath("text()").extract()[0].strip()
        else:
            item['price'] = "";
        if sel.css(".lvextras div.hotness-signal"):
            item['sold'] = sel.css(".lvextras div.hotness-signal").xpath("text()").extract()[0].strip()
        else:
            item['sold'] = ""
        item['image'] = sel.css('div.lvpic img').xpath("@src").extract()
        if sel.css('ul.lvdetails'):
            item['country'] = sel.css('ul.lvdetails').xpath("text()").extract()[0].strip()
        else:
            item['country'] = ""
            
        yield item
       
