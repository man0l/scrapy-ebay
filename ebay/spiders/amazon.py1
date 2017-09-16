# -*- coding: utf-8 -*-
#import scrapy
from scrapy_redis.spiders import RedisSpider
import re
from bs4 import BeautifulSoup
import lxml
from lxml.html.clean import Cleaner
import unicodedata
from ebay.items import AmazonItem
from lxml import etree
import uuid
import urllib2

class AmazonSpider(RedisSpider):
    name = "amazon_spider"
   

    def parse(self, response):
        #filename = str(uuid.uuid1()) + ".html"
        #open(filename, 'wb').write(response.body)
        p = re.compile("(\d+(\.\d+)?) out of \d+ stars")
        item = AmazonItem()
        
        item['title'] = response.css("#productTitle").xpath("text()").extract()[0]
        reviews = response.css(".reviewCountTextLinkedHistogram").xpath("@title").extract()[0]
        
        item['reviews'] = p.match(reviews).group(1)
        soldBySelector = response.css("#merchant-info a")
        if soldBySelector:
            soldBy = soldBySelector[0].xpath("text()").extract()[0]
            isFBA = 0
        else:
            p = re.compile("Ships from and sold by (Amazon)")            
            soldBy = response.css("#merchant-info").xpath("text()").extract()[0]
            m = p.search(soldBy)
            soldBy = m.group(1)
            isFBA = 1
               
        item['soldBy'] = soldBy
        item['isFBA']  = isFBA
        item['price'] = response.css("#price span.a-color-price")[0].xpath("text()").extract()[0].replace("$", "")
        item['availability'] = response.css("#availability span").xpath("text()").extract()[0].strip()
        m = re.compile("in stock", re.IGNORECASE).search(item['availability'])
        if m != None:
            item['isInStock'] = 1
        else:
            item['isInStock'] = 0
        
        shortDesc = "<ul>"
        for i in response.css("#feature-bullets li span"):
            shortDesc += "<li>" + i.xpath("text()").extract()[0] +"</li>"
        shortDesc += "</ul>"
        
        item['shortDesc'] = shortDesc
        item['longDescRaw'] = ""
        
        #item['longDescRaw'] = response.css("#productDescription .productDescriptionWrapper").extract()[0]
        if response.css("#productDescription"):
            item['longDescRaw'] = response.css("#productDescription").extract()[0]
            
            longDesc = item['longDescRaw']
            soup = BeautifulSoup(longDesc, 'lxml')         
            
            desc = re.compile("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s").split(soup.get_text())
            
        elif response.css(".a-container").xpath("script[contains(.,'ProductDescriptionIframeResize')]"):
            
            longDescSel = response.css(".a-container").xpath("script[contains(.,'ProductDescriptionIframeResize')]")                      
            longDesc = self.parseIframe(longDescSel.extract()[0])
            desc = re.compile("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s").split(longDesc)

        else:
            doc = lxml.html.fromstring(response.body)
            v = doc.cssselect(".a-container")[0]
            c = etree.tostring(v)
             
            longDesc = self.parseIframe(c)            
            desc = re.compile("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s").split(longDesc)

        
        longDesc = "<p>" + "".join(desc[0:3]) +"</p>"
        longDesc.replace("\n", "<br />")
        
        if not item['longDescRaw']:
            item['longDescRaw'] = longDesc
        
        
        item['longDesc'] = longDesc
        item['asin'] = response.css("#detail-bullets ul").xpath("li[contains(.,'ASIN')]/text()").extract()[0].strip()
        item['upc'] = ""
        upc = response.css("#detail-bullets ul").xpath("li[contains(.,'UPC')]/text()")
        self.logger.info(upc)
        if upc:
           upc = upc.extract()[0]
           item['upc'] = upc
           
        item['mpn'] = ""
        mpn = response.css("#detail-bullets ul").xpath("li[contains(.,'Item model number')]/text()")
        if mpn:
           mpn = mpn.extract()[0]
           item['mpn'] = mpn
        
        item['dimensions'] = ""
        dimensions = response.css("#detail-bullets ul").xpath("li[contains(.,'Product Dimensions')]/text()")
        if dimensions:
           dimensions = dimensions.extract()[0]
           item['dimensions'] = dimensions

        item['reviewsNum'] = ""
        reviewsNum = response.css("#acrCustomerReviewText")
        if reviewsNum:
           reviewsNum = reviewsNum.xpath("text()").extract()[0].replace(" customer reviews", "")
           item['reviewsNum'] = reviewsNum
        
        images = response.css("#imageBlock_feature_div").xpath("script").extract()[0]
        p = re.compile("hiRes\":\"(http://.*?)\"", re.DOTALL)
        item['image_urls'] = p.findall(images)
        
        yield item
        
    def parseIframe(self, html):
        p = re.compile("var iframeContent = \"(.*?)\"")
        m = p.search(html)
        a = m.group(1)
        a = self.cleanMe(urllib2.unquote(a))        
        
        doc = lxml.html.fromstring(a)
        v = doc.cssselect(".productDescriptionWrapper")[0]
        a = etree.tostring(v)
        a = unicode(a, "utf-8")
        soup = BeautifulSoup(a, "lxml")
        
        return soup.get_text().strip()
            
    def cleanMe(self, text):
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        #text = unicodedata.normalize("NFKD", text).encode('ascii','ignore')
        clean = cleaner.clean_html(text) 
        return clean

