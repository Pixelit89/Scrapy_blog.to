from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest
from scrapy import Request
from time import sleep
import re
from ..items import TorontoRestItem


class RestSpider(CrawlSpider):

    name = "rest_spider"

    allowed_domains = ['blogto.com']

    def start_requests(self):
        yield Request('http://www.blogto.com/api/v2/listings/?default_neighborhood=1', callback=self.parse)

    def parse(self, response):
        res = re.findall('"count":\d+,"next"', str(response.body))
        count = int(str(res)[10:-9])
        param = "&limit={}".format(count)
        yield Request("{0}{1}".format(response.url, param), callback=self.collect_links)

    def collect_links(self, response):
        raw_links = re.findall('"share_url":"http://www.blogto.com/.{1,50}","image_url"', str(response.body))
        clean_links = map(lambda x: x[13:-13], raw_links)
        for link in clean_links:
            sleep(8)
            yield SplashRequest(link, self.parse_item, args={'wait': 2.0})
        # yield SplashRequest('http://www.blogto.com/fashion/ewanika/', self.parse_item, args={'wait': 0.5})

    def parse_item(self, response):
        item = TorontoRestItem()
        item['business_name'] = response.xpath('//div[@class="listing-badge"]/div[@class="listing-badge-name"]/text()').extract_first()
        item['address'] = response.xpath('//a[@href="#address"]/text()').extract_first()
        item['phone'] = response.xpath('//a[@class="listing-badge-phone-link"]/text()').extract_first()
        item['website'] = response.xpath('//a[@class="listing-badge-website-link"]/@href').extract_first()
        item['location'] = response.xpath('//div[@class="listing-badge-detail-item listing-badge-neighborhood"]/a/text()').extract_first()
        item['category'] = response.xpath('//div[@class="listing-badge-category-info-label listing-badge-category-name"]/a/text()').extract_first()
        item['type'] = response.xpath('//div[@class="listing-badge-category-info-label listing-badge-sub-category-name"]/a/text()').extract_first()
        yield item