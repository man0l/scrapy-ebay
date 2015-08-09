from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

class TestSpider(CrawlSpider):
    name = "testproxy"
    domain_name = "whatismyip.com"
    start_urls = ["http://whatismyip.com"]

    def parse(self, response):
        open('test.html', 'wb').write(response.body)