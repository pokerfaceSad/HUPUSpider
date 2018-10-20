import datetime

import scrapy
from scrapy.spiders import CrawlSpider
import logging
from HUPUSpider.items import HUPUSpiderItem
from HUPUSpider import settings

# 虎扑PC端页面爬虫
class HUPUSpider_PC(CrawlSpider):
    name = "HUPUSpider_PC"

    def __init__(self, index_range,**kwargs):
        # 爬取页数
        self.index_range = int(index_range)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.cookies = {'_dacevid3': 'b5895dc0.05eb.3dcd.592d.9962d954a488', ' __gads': 'ID',
                        ' _HUPUSSOID': '64439a75-b83c-4fee-9344-0babfdd411cf',
                        ' _CLT': 'b0c2a05996d8b48b354e1fa4ddfc1fef',
                        ' AUM': 'dgHBUfku8xwDZEe86oW5OINHjN5nt-yqlWtWpTno5j7lw',
                        ' lastvisit': '0%091538046828%09%2Ferror%2F%40_%40.php%3F', ' __dacevid3': '0x3683874d5b7fd701',
                        ' sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221661b13e19d48d-0fd83f6a12964a-36664c08-1310720-1661b13e19e409%22%2C%22%24device_id%22%3A%221661b13e19d48d-0fd83f6a12964a-36664c08-1310720-1661b13e19e409%22%2C%22props%22%3A%7B%7D%7D',
                        ' __closeapp': '1',
                        ' _fmdata': 'qUwlDONI4Jo%2F11DhdIRbFPX5tfjVBD6rzrYqnTIJFidIu9OcNQ65NJPQL1rHRWID0BSm8sWCwhYqD7Ej8dUwvKh7LFoPLFrJwUzRfz%2BTOCQ%3D',
                        ' u': '39512754|TEJK55yf5Y6J5a6z|8cbd|7db5be365a7238b9c5bc366b8c20fada|5a7238b9c5bc366b|aHVwdV9lYjFiZTRmZmRkODA1MDM2',
                        ' us': '1ba2ab63fd935dd43f627e88c4a48b98c7c8cf5461e57af0735a165d7725dd3dadc375ff74471985db67209515af8727c444713ed46c19e8dc170a1a82f8d41c',
                        ' ua': '27967325',
                        ' _cnzz_CV30020080': 'buzi_cookie%7Cb5895dc0.05eb.3dcd.592d.9962d954a488%7C-1',
                        ' Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e': '1538149418,1538150353,1538150470,1538202857',
                        ' __dacevst': 'b031de8a.4281cfd3|1538204660134',
                        ' Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e': '1538202861'}

    def start_requests(self):
        for i in range(1, self.index_range + 1):
            # 有cookie的话可以设置cookie
            # scrapy.Request("http://www.xxxxxxx.com/user/login", meta={'cookiejar': 1}, headers=self.headers,
            #                callback=self.post_login)
            yield scrapy.Request('http://bbs.hupu.com/bxj-' + str(i), headers=self.headers, cookies=self.cookies)

    '''
    从论坛每一页解析出所有帖子的基本信息
    '''
    def parse(self, response):
        # 先提取出所有帖子 再根据类型不同进行分析
        post_list = response.xpath('//*[@id="ajaxtable"]/div[1]/ul/li')
        # 标题列表
        title_list = list()
        # 链接列表
        url_list = list()
        # 回复数列表
        reply_num_list = list()
        # 浏览量列表
        browse_list = list()
        # 作者ID列表
        authorID_list = list()
        # 发帖时间列表
        publish_time_list = list()

        for post in post_list:
            title_list.append(post.xpath('string(.//div[1]/a[@class])').extract()[0])
            url_list.append(post.xpath('./div[1]/a[@class]/@href').extract()[0])
            reply_num_list.append(post.xpath('./span/text()').extract()[0].split('\xa0/\xa0')[0])
            browse_list.append(post.xpath('./span/text()').extract()[0].split('\xa0/\xa0')[1])
            authorID_list.append(post.xpath('./div[2]/a[1]/text()').extract()[0])
            publish_time_list.append(post.xpath('./div[2]/a[2]/text()').extract()[0])

        for (title, url, reply_num, browse_num, authorID, publish_time) in zip(title_list, url_list, reply_num_list,
                                                                               browse_list, authorID_list,
                                                                               publish_time_list):
            item = HUPUSpiderItem()
            item["title"] = title
            item["url"] = url
            item['reply_num'] = reply_num
            item['browse_num'] = browse_num
            item['author'] = authorID
            item['publish_time'] = publish_time
            # 发起新的Request 获取帖子内容和亮评内容
            # 将还没有获取到帖子内容的Item通过meta传递
            yield scrapy.Request('http://bbs.hupu.com/' + url, meta={'tmpItem': item}, headers=self.headers,
                                 cookies=self.cookies, callback=self.parse_post)

    '''
    解析帖子内容
    '''
    def parse_post(self, response):
        # 帖子内容
        post_content = response.xpath('string(//*[@id="tpc"]/div/div[2]/table[1]/tbody/tr/td)').extract()[0]
        # 将帖子内容中无效字符滤除
        pass
        # 亮评列表
        bright_reply_list = response.xpath('//*[@id="readfloor"]/div')
        # 将亮评列表加工成字典类型
        # 亮评字典格式
        '''
        bright_reply_dict:
        {
            bright_reply_num:xx,
            bright_reply_1:
            {
                username:xxx,
                uid:xxx,
                bright_num:,
                reply_content
            },
            bright_reply_2:
            {
                username:xxx,
                uid:xxx,
                bright_num:,
                reply_content
            }


        }
        '''
        bright_reply_dict = {'bright_reply_num': len(bright_reply_list)}
        for index, bright_reply in enumerate(bright_reply_list):
            # 用户名
            username = bright_reply.xpath('.//div[@uname]/@uname').extract()[0]
            # 用户标识
            uid = bright_reply.xpath('.//div[@uname]/@uid').extract()[0]
            # 点亮数
            try:
                bright_num = bright_reply.xpath('.//*[@class="stime"]/text()').extract()[1]
            except BaseException as e:
                logging.error(e)
                logging.error("solving bright num occur an error")
                logging.error(bright_reply.extract()[0])
            # 评论内容
            try:
                reply_content = bright_reply.xpath('string(./div[2]/table/tbody/tr/td)').extract()[0]
            except BaseException as e:
                logging.error(e)
                logging.error("solving reply content occur an error")
                logging.error(bright_reply.extract()[0])

            bright_reply_dict['bright_reply_%d' % (index+1)] = {
                'username': username,
                'uid': uid,
                'bright_num': bright_num,
                'reply_content': reply_content,
            }
        item = response.meta['tmpItem']
        item['bright_reply_num'] = len(bright_reply_list)
        item['post_content'] = post_content
        item['bright_reply_dict'] = bright_reply_dict
        yield item

