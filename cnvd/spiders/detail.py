# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import json
from time import sleep
from random import randint

from redis import Redis
import scrapy
from scrapy import Request
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider

from cnvd.items import CnvdItem


class FlawSpider(scrapy.Spider):
    name = 'detail'
    allowed_domains = ['www.cnvd.org.cn']
    r = Redis()
    custom_settings = {
        # "LOG_LEVEL": "DEBUG",
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "__jsluid=7db4392c103877e06f152d3ef28e0973; JSESSIONID=7B0F6FC806B251013372FCD6E2B7E922; __jsl_clearance=1561000612.491|0|SOtmAGE%2FX9jGYli4h0SN9kyl64A%3D",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.cnvd.org.cn/flaw/typelist?typeId=29",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        },
        "ITEM_PIPELINES": {
            'cnvd.pipelines.CnvdDetailPipeline': 300,
        }
    }

    def start_requests(self):
        docs = self.r.srandmember("cnvd:meta", number=100)
        for doc in docs:
            item = json.loads(doc)
            item = CnvdItem(**item)
            cnvd_id = item["id"]
            if self.r.sismember("detail:crawled", cnvd_id):
                continue
            url = item["detail"]

            yield Request(
                url=url, 
                meta={"item": item},
                dont_filter=True,
                )
            

    def parse(self, response):
        if response.body_as_unicode() == "":
            raise CloseSpider("Blank Respond")
        item = response.meta["item"]
        rows = response.xpath('//table[@class="gg_detail"]/tbody/tr')
        detail = {}
        for row in rows:
            tds = row.xpath('.//td')
            if len(tds) < 2:
                continue
            key = tds[0].xpath("./text()").extract_first()
            value = tds[1].xpath(".//text()").extract()
            value = "".join(i.strip() for i in value)
            detail[key.strip()] = "".join(value.split())
        item["detail"] = detail
        yield item
