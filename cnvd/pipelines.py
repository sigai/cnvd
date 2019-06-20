# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class CnvdMetaPipeline(object):
    def process_item(self, item, spider):
        spider.r.sadd("cnvd:meta", json.dumps(dict(item), ensure_ascii=False))
        return item


class CnvdDetailPipeline(object):
    def process_item(self, item, spider):
        spider.r.sadd("cnvd:detail", json.dumps(dict(item), ensure_ascii=False))
        spider.r.sadd("detail:crawled", item["id"])
        return item
