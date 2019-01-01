from pymongo import MongoClient
import settings


class DataGetter(object):
    def __init__(self, date, query_factor, result_format, mode_select):
        self.date = date
        self.query_factor = query_factor
        self.result_format = result_format
        self.collection = self.connect()
        if mode_select == 1:  # 模式选择
            self.table, self.size = self.get_data(0.05)  # 取每天 Rank 前%5的帖子
        else:
            self.table, self.size = self.get_data(1)  # 取每天所有的帖子

    @staticmethod
    def connect():
        '''
        :return:  Database中的集合
        '''
        client = MongoClient('mongodb://%s:%s@%s:%s/' % (settings.User_Id, settings.User_Password, settings.Server_IP,
                                                         settings.Server_Port))  # 连接到服务器
        db_list = client.database_names()
        for db in db_list:  # 找到Spider数据库
            if db == "%s" % settings.DataBase_Name:
                data_base = client.get_database(db)
            else:
                continue
        # 获取集合 存储到列表中
        db_collection = data_base.get_collection("%s" % settings.Collection_Name)
        return db_collection

    def get_data(self, alpha):

        '''
        Function Get_data is to get One Day Docs according to  actual Conditions
        :param alpha is mode_select parameter to insure the size of the returned post in one day
        '''
        print("Query Database Start: Date = %s" % self.date)
        table = []
        docs = self.collection.find(self.query_factor, self.result_format)
        size = docs.count()
        print("Query Database Finished: Date = %s, Size=%d" % (self.date, size))
        print("Start sort posts...")
        docs = docs.sort([("bright_reply_num", -1), ("reply_num", -1), ("browse_num", -1)])
        print("Sort posts finshed")
        #  先按照帖子的回复数 再按照点亮数和浏览量进行 降序
        for i in range(0, round(alpha*size)):  # 取当天的总的帖子的Rank前 5% 的数据
            Dict = docs[i]
            table.append(Dict)
        print("Get hot post Finished: size=%d" % round(alpha*size))
        return table, round(alpha*size)
