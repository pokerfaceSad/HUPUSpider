from scrapy.spiders import CrawlSpider

from HUPUSpider.items import HUPUSpiderItem

# 虎扑移动端端页面爬虫
class HUPUSpider_M(CrawlSpider):
    name = "HUPUSpider_M"
    start_urls = ['https://m.hupu.com/bbs/34',
                  'https://bbs.hupu.com/bxj-2',
                  'https://bbs.hupu.com/bxj-3']


    def parse(self, response):
        # 标题列表
        titile_list = response.xpath('/html/body/section[2]/div[2]/ul/li/a/div/div/h3/text()').extract()
        # 链接列表
        url_list = response.xpath('/html/body/section[2]/div[2]/ul/li/a/@href').extract()
        url_list = list(map(lambda x: x.split('//m.hupu.com/bbs')[1], url_list))
        # 亮评数列表
        bright_comment_num_list = response.xpath('/html/body/section[2]/div[2]/ul/li/a/div/div/div/div[3]/span[1]/text()').extract()
        # 浏览量列表
        comment_num_list = response.xpath('/html/body/section[2]/div[2]/ul/li/a/div/div/div/div[3]/span[2]/text()').extract()
        # 作者ID列表
        authorID_list = response.xpath('/html/body/section[2]/div[2]/ul/li/a/div/div/div/div[2]/text()').extract()
        authorID_list = list(map(lambda x: x[1:-1], authorID_list))
        # 发帖时间列表
        publih_time_list = response.xpath('//*[@id="ajaxtable"]/div[1]/ul/li/div[2]/a[2]/text()').extract()

        for (title,url,reply_num,browse_num,authorID,publish_time) in zip(title_list,url_list,reply_num_list,browse_list,authorID_list,publih_time_list):
            item = HUPUSpiderItem()
            item["title"] = title
            item["url"] = self.start_urls[0]+url
            item['reply_num'] = reply_num
            item['browse_num'] = browse_num
            item['author'] = authorID
            item['publish_time'] = publish_time

            yield item
