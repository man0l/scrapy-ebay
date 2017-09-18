from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

class TestSpider(CrawlSpider):
    name = "testproxy"
    domain_name = "check.torproject.org"
    start_urls = ["https://check.torproject.org/"]

    def parse(self, response):
        open('test.html', 'wb').write(response.body)