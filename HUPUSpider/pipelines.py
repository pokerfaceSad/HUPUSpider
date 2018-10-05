# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from HUPUSpider import settings
import pymongo
import configparser

class HupuspiderPipeline(object):
    def __init__(self):
        # self.file = codecs.open('D:/article.json', 'w', encoding="utf-8")
        # self.cfg = configparser.ConfigParser()
        # self.cfg.read('D:\MyFiles\ScraTest\HUPUSpider\HUPUSpider\spider.conf')
        # print(self.cfg.sections())
        # url = "mongodb://%s:%s@%s:%s/" % (self.cfg.get('db', 'db_user'), self.cfg.get('db','db_pwd'), self.cfg.get('db', 'db_host'), self.cfg.get('db', 'db_port'))
        url = "mongodb://%s:%s@%s:%s/" % (settings.db_user, settings.db_pwd, settings.db_host, settings.db_port)
        self.dbClient = myclient = pymongo.MongoClient(url)
        mydb = self.dbClient["HUPU_DB"]
        self.mycol = mydb["POST_COL"]

    def process_item(self, item, spider):
        # lines = json.dumps(dict(item), ensure_ascii=False) + "\n"  # 确保中文显示正常
        # self.file.write(lines)
        temp = dict(item)
        temp['_id'] = temp['url']
        # 采用save保存可以将旧的数据覆盖掉
        self.mycol.save(temp)
        return item

    def spider_closed(self, spider):
        # self.file.close()
        self.dbClient.close()