# -*- coding: utf-8 -*-
import scrapy
import urllib
from ebay.items import EbayItem
import urlparse
import re


class EbaySpiderSpider(scrapy.Spider):
    name = "ebay_spider"
    allowed_domains = ["ebay.com"]
    #start_urls = ["http://www.ebay.com"]
    start_urls = [
				  #"https://www.ebay.com/sch/Halloween/170094/i.html?_from=R40&_nkw=halloween&_ipg=200&LH_PrefLoc=1", 
				  # home and garden - yard and outdoor
				  #"https://www.ebay.com/sch/Yard-Garden-Outdoor-Living/159912/i.html?_from=R40&_ipg=200&_nkw=halloween&LH_PrefLoc=1"
				  #"https://www.ebay.com/sch/Garden-Decor/20498/i.html?_from=R40&_nkw=halloween&LH_PrefLoc=1&_ipg=200"
				  # "https://www.ebay.com/sch/Statues-Lawn-Ornaments/29511/i.html?_from=R40&_nkw=halloween&LH_PrefLoc=1&_ipg=200"
				  #"https://www.ebay.com/sch/Yard-Garden-Outdoor-Living/159912/i.html?_from=R40&_nkw=halloween&LH_PrefLoc=1&_ipg=200"
				  #"https://www.ebay.com/sch/Halloween/170094/i.html?_from=R40&_nkw=halloween&rt=nc&LH_PrefLoc=1&_ipg=200"
				  #"https://www.ebay.com/b/Blankets-Throws/175750/bn_2310726"
				  #"https://www.ebay.com/b/Holiday-Seasonal-Decor/38227/bn_1852123"
				  "https://www.ebay.com/b/Halloween-Decor/170094/bn_1853886?_udlo=5&LH_ItemCondition=1000&LH_PrefLoc=1&LH_BIN=1"
				  ]
	
    def parse(self, response):
      for sel in response.css('ul.b-list__items_nofooter li.s-item'):
        item = EbayItem()
        item['link'] = sel.css('.s-item__link').xpath("@href").extract_first()
        item['sold'] = sel.css('.s-item__hotness span').xpath("text()").extract_first()
        if item['sold']:
          yield item
        
      pagination = response.css('.ebayui-pagination__control[rel=next]').xpath("@href").extract_first()
      #self.logger.info("Pagination URL next page "+pagination) 
      if pagination:
        yield response.follow(pagination, self.parse)
	
    def parse2(self, response):
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
		
      pagination = re.search('<a.*?class="gspr next" href="(.*)">', response.body)
	  
      if pagination:
	  
		yield response.follow(pagination.group(1), self.parse)
      
	
    def parse1(self, response):	
      trksid = response.css("input[type='hidden'][name='_trksid']").xpath("@value").extract()[0]       
      with open('/app/ebay/product_names.txt') as fp:
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
       
