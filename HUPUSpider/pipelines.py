# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from HUPUSpider import settings
import pymongo

class HupuspiderPipeline(object):
    def __init__(self):
        url = "mongodb://%s:%s@%s:%s/" % (settings.db_user, settings.db_pwd, settings.db_host, settings.db_port)
        self.dbClient = myclient = pymongo.MongoClient(url)
        mydb = self.dbClient["HUPU_DB"]
        self.mycol = mydb["POST_COL"]

    def process_item(self, item, spider):
        temp = dict(item)
        temp['_id'] = temp['url']
        # 采用save保存可以将旧的数据覆盖掉
        self.mycol.save(temp)
        return item

    def spider_closed(self, spider):
        # self.file.close()
        self.dbClient.close()