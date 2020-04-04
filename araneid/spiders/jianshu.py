# -*- coding: utf-8 -*-
import scrapy

from araneid.items import JianshuItem


class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['www.jianshu.com']
    start_urls = [
        'https://www.jianshu.com/recommendations/users?page=1'
    ]
    custom_settings = {
        # 'LOG_LEVEL': 'DEBUG',
        # 'LOG_FILE': '5688_log_%s.txt' % time.time(),
        "DEFAULT_REQUEST_HEADERS": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'X-PJAX': 'true'
        }
    }

    def __init__(self):
        self.page = 1

    def parse(self, response):
        content = response.body

        for val in response.xpath('//div[@class="wrap"]/a[1]'):
            user_out_url = val.xpath('./@href').extract()[0]
            user_name = val.xpath('./h4/text()').extract()[0].strip()

            item = JianshuItem()
            item['user_out_url'] = user_out_url
            item['user_name'] = user_name
            yield item

        self.page += 1
        if content is not None:
            url = 'https://www.jianshu.com/recommendations/users?page=' + str(self.page)
            yield scrapy.Request(url, callback=self.parse)

