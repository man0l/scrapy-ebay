# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from amazonproduct import API
from amazonproduct.errors import NoExactMatchesFound
import re
from time import sleep
from dandelion import DataTXT
from dandelion.base import DandelionException
from scrapy.conf import settings
from twisted.enterprise import adbapi
from scrapy import log
from datetime import datetime
from hashlib import md5

class AmazonPipeline(object):

    
    def __init__(self):
        self.api = API(locale='us')
        self.datatxt = DataTXT(app_id=settings['DANDELION_APP_ID'], app_key=settings['DANDELION_KEY'])

        
    def process_item(self, item, spider):
        if spider.name in ['ebay_spider', 'amazon_spider']:
            return item
        item['asin'] = []    
                    
        if 'upc' in item:
          if item['upc']: 
            asin = self.get_upc(item['upc'])               
            item['asin'] = asin
        
        elif 'ean' in item:
          if item['ean']:
            asin = self.get_ean(item['ean'])
            item['asin'] = asin
        elif False and 'mpn' in item and 'brand' in item:
          if item['mpn'] and item['brand']:
            asin = self.search("%s+%s" % (item['mpn'], item['brand']), item['description'])
            item['asin'] = asin
        elif 'mpn' in item and 'brand' in item:
          if item['mpn'] and item['brand']:
            asin = self.search("%s+%s" % (item['mpn'], item['brand']), item['description'])
            item['asin'] = asin

            
        
        return item
        
    def get_upc(self, upc):        
        response = self.api.item_lookup(upc, SearchIndex="Blended", IdType="UPC")
  
        asin = list()
        
        for amazon_item in response.Items.Item:
             asin.append(unicode(amazon_item.ASIN.text, 'utf-8'))
        
        return asin        
        
    def get_ean(self, ean):
        response = self.api.item_lookup(ean, SearchIndex="Blended", IdType="EAN")
  
        asin = list()
        
        for amazon_item in response.Items.Item:
             asin.append(unicode(amazon_item.ASIN.text, 'utf-8'))
        
        return asin        
        
    def search(self, keyword, description):
        asin = list()
        try:
            response = self.api.item_search("Blended", Keywords=keyword, ResponseGroup="EditorialReview")        
        except NoExactMatchesFound:
            return asin             
            
        #if 'response' in locals() and response.results >=1:
            for amazon_item in response:
                # start matching the editorial review
                if hasattr(amazon_item, "EditorialReviews") and hasattr(amazon_item.EditorialReviews, "EditorialReview"):
                    match = self.find_match(description, amazon_item.EditorialReviews.EditorialReview.Content.text)
                    if float(match) > 70.00 :
                        asin.append(unicode(amazon_item.ASIN.text, 'utf-8'))
            return asin
        
        
    def find_match(self, source, dest):        
        paragraphs = list()
        match  = list()
        
        for line in source.splitlines(): 
          if len(line) > 20:
            paragraphs.append(line)
            
        paragraphs = paragraphs[0:5]
        try:
            for p in paragraphs:     
                response = self.datatxt.sim(p, dest)
                match.append(response.similarity)
        except DandelionException:             
            return 0.00
        
        match.sort(reverse=True)
        
        return match[0]
        
        
class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
    
        if spider.name in ['ebay_spider', 'amazon_spider']:
            return item
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        guid = item['ebayID']
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        asin = ",".join(item['asin'])

        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM item WHERE ebay_id = %s
        )""", (guid, ))
        ret = conn.fetchone()[0]
         
        if ret:
            conn.execute("""
                UPDATE item
                SET upc=%s, mpn=%s, brand=%s, ean=%s, url=%s, description=%s, price=%s, category=%s, asin=%s, created_at=%s
                WHERE ebay_id=%s
            """, (item['upc'] if item['upc'] else '', item['mpn'] if item['mpn'] else '', item['brand'] if item['brand'] else '', item['ean'] if item['ean'] else '', item['url'], item['description'],item['price'],item['category'], asin, now, guid))
            spider.log("Item updated in db: %s %r" % (guid, item))
            
            conn.execute("""
                SELECT id FROM item WHERE ebay_id = %s
            """, (guid, ))
            item_id = conn.fetchone()[0]
 
            conn.execute("""
                DELETE FROM item_sold WHERE ebay_id=%s and item_id=%s
            """, (guid, item_id))
            if item.get('sold_items', None) is not None:
                self._insert_sold(conn, item['sold_items'], item_id)
            

            
        else:
            conn.execute("""
                INSERT INTO item SET upc=%s, mpn=%s, brand=%s, ean=%s, url=%s, description=%s, price=%s, category=%s, asin=%s, created_at=%s, ebay_id=%s
            """, (item.get('upc', ''), item.get('mpn', ''), item.get('brand', ''), item.get('ean', ''), item['url'], item['description'],item['price'],item['category'], asin, now, guid))
            
            conn.execute("""
                SELECT LAST_INSERT_ID() as id
            """)
            item_id = conn.fetchone()[0]

            if item.get('sold_items', None) is not None:
              self._insert_sold(conn, item['sold_items'], item_id)

                        
            spider.log("Item stored in db: %s %r" % (guid, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)
        
    def _insert_sold(self, conn, sold_items, item_id):
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        for sold in sold_items:
            conn.execute("""
                INSERT INTO item_sold SET price=%s, quantity=%s, date_at=%s, ebay_id=%s, item_id=%s, created_at=%s
            """, (float(sold['price']), int(sold['quantity']), sold['date'], sold['ebayID'], item_id, now ))

