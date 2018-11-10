from pymongo import MongoClient
import settings

client = MongoClient('mongodb://%s:%s@%s:%s/' % (settings.User_Id, settings.User_Password, settings.Server_IP,
                                                 settings.Server_Port))  # 连接到服务器
db_list = client.list_database_names()
for db in db_list:  # 找到Spider数据库
    if db == 'HUPU_DB':
        data_base = client.get_database(db)
    else:
        continue

# 异常处理
try:
    coll_names = data_base.list_collection_names()  # 列举数据库中的集合
except ValueError:
    raise

# 只有一个collection
# 获取集合 存储到列表中
db_collection = data_base.get_collection(coll_names[0])

# 首先按照帖子的发帖日期(publish_time),回复数(reply_num)，以及被点亮的评论数(bright_reply_num)进行筛选


def get_data(filter_conf1, filter_conf2):

    '''
    Function Get_data is to get Docs according to  actual Conditions
    Input: Filter Condition
    '''
    table = []
    size = db_collection.find(filter_conf1, filter_conf2).count()
    docs = db_collection.find(filter_conf1, filter_conf2).sort\
        ([("reply_num", -1), ("bright_reply_num", -1), ("browse_num", -1)])
    #  先按照帖子的回复数 再按照点亮数和浏览量进行 降序
    for i in range(0, round(0.05*size)):  # 取当天的总的帖子的Rank前 5% 的数据
        Dict = docs[i]
        table.append(Dict)
    return table, round(0.05*size)
