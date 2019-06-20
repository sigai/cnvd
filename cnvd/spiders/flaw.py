# -*- coding: utf-8 -*-
from urllib.parse import urlencode

from redis import Redis
import scrapy
from scrapy import Request
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider

from cnvd.items import CnvdItem


class FlawSpider(scrapy.Spider):
    name = 'flaw'
    allowed_domains = ['www.cnvd.org.cn']
    base_url = "https://www.cnvd.org.cn"
    url = "https://www.cnvd.org.cn/flaw/typeResult?"
    r = Redis(decode_responses=True)
    custom_settings = {
        "LOG_LEVEL": "INFO",
        "ITEM_PIPELINES": {
            'cnvd.pipelines.CnvdMetaPipeline': 300,
        }
    }

    def start_requests(self):
        self.r.sdiffstore("cnvd:offset", "cnvd:offset", "offset:crawled")
        offsets = self.r.srandmember("cnvd:offset", number=500)
        for offset in offsets:            
            if offset is None:
                break
            parameters = {
                "typeId": 29,
                "max": 20,
                "offset": offset,
            }
            yield Request(
                url=self.url+urlencode(parameters), 
                meta={"parameters": parameters},
                dont_filter=True,
                )

    def parse(self, response):
        if response.body_as_unicode() == "":
            raise CloseSpider("Blank Respond")
        parameters = response.meta["parameters"]
        offset = parameters.get("offset", None)
        rows = response.xpath('//table[@class="tlist"]/tbody/tr')
        for row in rows:
            item = CnvdItem()
            tds = row.xpath('.//td')
            link = tds[0].xpath("./a/@href").extract_first()
            title = tds[0].xpath('./a/@title').extract_first()
            rank = tds[1].xpath('./text()').extract()
            click = tds[2].xpath('./text()').extract_first()
            comment = tds[3].xpath('./text()').extract_first()
            follow = tds[4].xpath('./text()').extract_first()
            public_time = tds[5].xpath('./text()').extract_first()
            item["id"] = link.strip().split("/")[-1]
            item["title"] = title.strip()
            item["click"] = click.strip()
            item["rank"] = "".join(i.strip() for i in rank)
            item["comment"] = comment.strip()
            item["follow"] = follow.strip()
            item["public_time"] = public_time.strip()
            item["detail"] = self.base_url + link.strip()
            yield item
        else:
            if offset:
                self.r.sadd("offset:crawled", offset)