from Data_Preprocessing.Get_Data import DataGetter
from Data_Preprocessing.Date_Increase import date_increase


# Filter_Conf1为对Value值的筛选  Filter_Conf2确定了需要映射的数据 设置初始的Filter_Conf
# 对于不同日期的帖子 很难确定回复数 点亮数 浏览数的门限值


def filtered_data(date, n, mode):
    '''
    :param date: Query 的初始日期
    :param n: 需要查询的天数
    :param mode:查询模式选择
    :return: Collection：返回所有的帖子的集合, Size_Post:返回的每天的帖子的数量, Date_List：查询的日期列表
    '''
    # 存储分配
    collection = []
    size_post = []
    date_list = []
    i = 0  # Control Iteration Times
    while i < n:
        query_factor = {"crawl_time": {"$regex": r"^.*%s.*$" % date}, "reply_num": {"$gt": 0},
                       "bright_reply_num": {"$gt": 0}, "browse_num": {"$gt": 0}}
        result_format = {"url": 0, "publish_time": 0}  # 确定需要映射的返回参数
        get_object = DataGetter(date, query_factor, result_format, mode)  # 创建GetData实例
        table, size = get_object.table, get_object.size  # 通过属性访问
        if size == 0:  # 如果获取到的帖子的长度为0：日期超出了集合的Index
            #  触发日期Index 不对的异常
            if i != n:
                raise Exception("%s Out Date Index" % date)
        else:
            collection.append(table)
            size_post.append(size)
            date_list.append(date)
            print("Collect the %d Day Over:" % (i + 1))
            i = i + 1
        temp_list = date.split('-')
        temp_list = [int(x) for x in temp_list]  # 字符串转整型变量
        # 天数加一 假定数据中的日期的Value是正确的
        temp_list = date_increase(temp_list)  # 得到数据中日期增加的列表
        for j in range(0, len(temp_list)):
            if j == 0:
                temp_list[j] = str(temp_list[j])
            else:
                if 0 < temp_list[j] < 10:
                    temp_list[j] = str("0%s" % temp_list[j])  # 保证日期的格式的一致性
                else:
                    temp_list[j] = str(temp_list[j])
        separator = '-'
        temp_list = separator.join(temp_list)
        date = temp_list
    return collection, size_post, date_list




