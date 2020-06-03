# -*- coding: utf-8 -*-
import scrapy
from ..items import Hc360Item



class HcSpider(scrapy.Spider):
    name = 'hc'
    # allowed_domains = ['hc360.com']
    base_letter_url = 'http://top.hc360.com/{}-1.html'
    base_https = 'https:'

    def start_requests(self):
        for i in range(97, 123):
            yield scrapy.Request(url=self.base_letter_url.format(chr(i)))

    def parse(self, response):

        next_page = response.xpath('//a[@title="下一页"]/@href').get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

        hot_words = response.xpath('//ul[@class="industry_word"]/li//a/@href').getall()
        for hot_word in hot_words:
            yield scrapy.Request(url=hot_word, callback=self.parse_hotword)

    def parse_hotword(self, response):
        detail_hrefs = response.xpath('//dd[@class="newName"]/a/@href').getall()
        for detail_thing in detail_hrefs:
            yield scrapy.Request(url=self.base_https+detail_thing, callback=self.detail)

        hotsearchs = response.xpath('//div[@class="navRig"]/dl/dd/a/@href').getall()
        for hotsearch in hotsearchs:
            yield scrapy.Request(url=self.base_https+hotsearch, callback=self.parse_hotword)

        more = response.xpath('//a[@title="查看更多"]/@href').get()
        if more:
            yield scrapy.Request(url=self.base_https+more, callback=self.more_things)

    def more_things(self, response):
        things = response.xpath('//div[@class="seaNewList"]/dl/dd/a/@href').getall()
        for thing in things:
            yield scrapy.Request(url=self.base_https+thing, callback=self.detail)
        next_page = response.xpath('//a[@title="下一页"]/@href').get()
        if next_page:
            yield scrapy.Request(url=self.base_https+next_page, callback=self.more_things)

    def detail(self, response):
        # print(response.url)

        mobile = '空'
        tele = '空'
        cont_person = '空'
        com_name = '空'

        uls = response.xpath('//ul[@class="card_list"]/li')
        for li in uls:
            if li.xpath('p[1]/text()').get() == '手机号码：':
                mobile = li.xpath('p[2]/text()').get()

            if li.xpath('p[1]/text()').get() == '座机电话：':
                tele = li.xpath('p[2]/text()').get().replace('\xa0','')

            if li.xpath('p[1]/text()').get() == '联系人：':
                cont_person = li.xpath('p[2]/text()').get().strip().replace(' ','').replace('\n','').replace('\r','').replace('\t','').split('\xa0')[0]

            if li.xpath('p[1]/text()').get() == '公司名称：':
                com_name = li.xpath('p[2]/text()').get()
        print(mobile, tele, cont_person, com_name)

        item = Hc360Item()
        item['mobile'] = mobile
        item['tele'] = tele
        item['cont_person'] = cont_person
        item['com_name'] = com_name
        yield item

