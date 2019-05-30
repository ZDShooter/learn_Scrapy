# -*- coding: utf-8 -*-
import scrapy
from TcMap.items import TcMapItem


class InfoSpiderSpider(scrapy.Spider):
    name = 'info_spider'
    allowed_domains = ['www.tcmap.com.cn']
    base_url = 'http://www.tcmap.com.cn'
    start_urls = [base_url]

    def parse(self, response):
        # 获取所有省会地址
        res_url_list = response.xpath("//div[@class='ht']/b/a/@href").extract()
        # 返回所有的省级url，用parse1回调
        for each_url in res_url_list:
            full_url = self.base_url + str(each_url)
            yield scrapy.Request(full_url, callback=self.parse_province)

    def parse_province(self, response):
        # 获取下级url地址列表,并返回
        next_url_list = response.xpath("//td/strong/a[@class='blue']")
        # 获取省会代码，名称
        area_code = response.xpath("//tr/td/text()").extract()[5]
        area_name = response.xpath("//div[@class='ht']/span[@class='title1']/a/strong/text()").extract()[0]
        area_profile = response.xpath("//td[@valign='top']/text()").extract()
        # 循环返回下级url地址
        for each_url in next_url_list:
            url_ = each_url.xpath("./@href").extract()[0]
            next_url = self.base_url + str(url_)
            yield scrapy.Request(next_url, callback=self.parse_next)
        # 定义Item字段
        item = TcMapItem()
        # 获取省会代码
        item["fileCode"] = area_code[1:4]
        # 获取文件名
        item["fileName"] = area_name[:-2]
        # 获取简介
        item["fileContent"] = area_profile
        # 返回item
        yield item

    def parse_next(self, response):
        # 获取下级url地址列表
        next_url_list = response.xpath("//tr/td[@align='center']/strong/a")
        # 获取文件名
        area_code = response.xpath("//tr/td/text()")[2].extract()
        area_name = response.xpath("//tr/td/text()")[0].extract()
        area_profile = response.xpath("//*[@id='page_left']/div[6]/text()").extract()
        # 判断是否位街道和乡镇以上行政区域以及是否存在下级行政区域
        if (len(area_code) < 9) and next_url_list:
            for each_url in next_url_list:
                next_url = self.base_url + str(each_url.xpath("./@href").extract()[0])
                yield scrapy.Request(next_url, callback=self.parse_next)
        else:
            pass
        # 定义Item字段
        item = TcMapItem()
        # 获取区域代码
        item["fileCode"] = area_code[1:]
        # 获取地域名称
        item["fileName"] = area_name[1:]
        # 获取简介
        item["fileContent"] = area_profile
        yield item
