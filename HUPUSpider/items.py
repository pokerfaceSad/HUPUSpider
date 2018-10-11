# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HUPUSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 帖子标题
    title = scrapy.Field()
    # 帖子链接
    url = scrapy.Field()
    # 回复数量
    reply_num = scrapy.Field()
    # 浏览数
    browse_num = scrapy.Field()
    # 亮评数
    bright_reply_num = scrapy.Field()
    # 楼主ID
    author = scrapy.Field()
    # 发帖时间
    publish_time = scrapy.Field()
    # 帖子内容
    content = scrapy.Field()
    # 亮评列表
    bright_reply_list = scrapy.Field()

