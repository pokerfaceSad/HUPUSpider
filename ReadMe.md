# HUPUSpider
虎扑步行街舆情监控

对虎扑步行街某一天的用户发帖及评论进行分析，采用NLP的方法提取出每个帖子的关键词，生成词云

![2018-11-11分析结果][1]
# 结构
数据采集使用Scrapy框架，存储使用MongoDB，数据处理采用[jieba][3]和[WordCloud][4]
![系统结构][2]

# 数据抓取
爬虫使用[Scrapy框架][5]编写，采用[SpiderKeeper][6]进行管理，设置一个定时任务每半小时抓取论坛首页的所有帖子的

 - 标题
 - url
 - 楼主ID
 - 回复数量
 - 浏览量
 - 发帖时间
 - 主贴内容
 - 亮评内容

为了方便数据分析，在每次抓取时都对数据的**crawl_time**字段进行更新，记录数据的抓取时间。
# 数据存储
考虑到数据格式的复杂性，采用非关系型数据库MongoDB
数据样例如下

    {
    "_id" : "/24213454.html",
    "title" : "认真脸：日韩医术那么发达，增高手术也是没问题的吧",
    "url" : "/24213454.html",
    "reply_num" : 98,
    "browse_num" : 21963,
    "author" : "可惜不是金牛座",
    "publish_time" : "2018-11-03",
    "crawl_time" : "2018-11-03 16:30,2018-11-03 17:00",
    "bright_reply_num" : 8,
    "post_content" : "帖子内容....",
    "bright_reply_dict" : {
        "bright_reply_num" : 8,
        "bright_reply_1" : {
            "username" : "CZ_Miles",
            "uid" : "195790169801066",
            "bright_num" : "262",
            "reply_content" : "亮评内容..."
        },
        /*省略下面的7条亮评*/
     }
   

# 数据分析

## 一、数据获取
1. 将帖子的**crawl_time**字段作为查询条件，从数据库查询得到目标天的所有帖子。为了避免一些水贴影响分析效果，在查询条件中设置：
 - 帖子的回复数需要大于0
 - 帖子的被点亮的回复数需要大于0
 - 帖子的浏览量需要大于0
2. 对第一步查询到的结果，按照帖子的**亮评数量**对帖子排序（点亮数相同的再比较评论数量，评论数量相同的再比较浏览量），取排名前5%的帖子作为待分析的数据


## 二、数据处理
1. 考虑到帖子中可能有一些无意义的字符（如客户端自带的评论小尾巴），对每一个帖子用正则表达式去掉其中的无效内容 
2. 对每个帖子的文本内容（帖子正文和亮评）采用中文语言处理工具[jieba分词][7]中的关键词提取算法**TF-IDF**提取其关键词，为了使处理的效果更好，添加了**停用词表**和**大概率成词表**进行修正
3. **关键词权重**（在词云中的大小）取决于所属帖子的热度

    关键词权重计算公式：

        0.4995*帖子的点亮数+0.4995*帖子的被点亮的评论的平均点亮数+0.001*帖子的回复数

    最后将给关键词-权重封装成字典类型


## 三、结果可视化
   使用[WordCloud][8]将上一步骤得到的关键词-权重字典生成词云

# To Be Continued


  [1]: https://raw.githubusercontent.com/pokerfaceSad/HUPUSpider/master/img/2018-11-11%E5%88%86%E6%9E%90%E7%BB%93%E6%9E%9C.png
  [2]: https://raw.githubusercontent.com/pokerfaceSad/HUPUSpider/master/img/struct.png
  [3]: https://github.com/fxsjy/jieba
  [4]: http://amueller.github.io/word_cloud/index.html
  [5]: https://github.com/scrapy/scrapy
  [6]: https://github.com/DormyMo/SpiderKeeper
  [7]: https://github.com/fxsjy/jieba
  [8]: http://amueller.github.io/word_cloud/index.html
