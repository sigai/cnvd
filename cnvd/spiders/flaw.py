# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import base64
import random

from redis import Redis
import scrapy
from scrapy import Request
from scrapy.utils.project import get_project_settings

from cnvd.items import CnvdItem


class FlawSpider(scrapy.Spider):
    name = 'flaw'
    allowed_domains = ['www.cnvd.org.cn']
    base_url = "https://www.cnvd.org.cn"
    url = "https://www.cnvd.org.cn/flaw/typeResult?"
    r = Redis()
    settings = get_project_settings()
    proxy_server = settings.get("PROXY_SERVER")
    proxy_user = settings.get("PROXY_USER")
    proxy_pass = settings.get("PROXY_PASS")
    proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((proxy_user + ":" + proxy_pass), "ascii")).decode("utf8")

    def start_requests(self):
        parameters = {
            "typeId": 29,
            "max": 20,
            "offset": 0,
        }
        yield Request(
            url=self.url+urlencode(parameters), 
            meta={"parameters": parameters},
            dont_filter=True,
            callback=self.parse_start,
            )

    def parse_start(self, response):
        parameters = response.meta["parameters"]
        offset = parameters.get("offset", None)
        total = response.xpath('//span[not(@class)]').re(r"共\xa0(.*)\xa0条")[0]
        while True:
            parameters["offset"] += parameters["max"]
            yield Request(
                url=self.url+urlencode(parameters), 
                meta={"parameters": parameters},
                dont_filter=True,
                callback=self.parse_list)
            break
    
    def parse_list(self, response):
        rows = response.xpath('//table[@class="tlist"]/tbody/tr')
        for row in rows:
            item = CnvdItem()
            tds = row.xpath('.//td')
            link = tds[0].xpath("./a/@href").extract_first()
            title = tds[0].xpath('./a/@title').extract_first()
            click = tds[1].xpath('./text()').extract_first()
            rank = tds[2].xpath('./text()').extract_first()
            comment = tds[3].xpath('./text()').extract_first()
            follow = tds[4].xpath('./text()').extract_first()
            public_time = tds[5].xpath('./text()').extract_first()
            item["id"] = link.strip().split("/")[-1]
            item["title"] = title.strip()
            item["rank"] = rank.strip()
            item["comment"] = comment.strip()
            item["follow"] = follow.strip()
            item["public_time"] = public_time.strip()
            
            yield Request(
                url=self.base_url+link, 
                meta={"item": item},
                dont_filter=True,
                callback=self.parse)
    
    def parse(self, response):
        item = response.meta["item"]
        rows = response.xpath('//table[@class="gg_detail"]/tbody/tr')
        detail = {}
        for row in rows:
            tds = row.xpath('.//td')
            if len(tds) < 2:
                continue
            key = tds[0].xpath("./text()").extract_first()
            value = tds[1].xpath(".//text()").extract_first()
            detail[key] = value
        item["detail"] = detail
        yield item
            


     
