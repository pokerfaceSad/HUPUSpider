from Data_Preprocessing.Get_Data import GetData
from Data_Preprocessing.Date_Increase import date_increase


# Filter_Conf1为对Value值的筛选  Filter_Conf2确定了需要映射的数据 设置初始的Filter_Conf
# 对于不同日期的帖子 很难确定回复数 点亮数 浏览数的门限值


def filtered_data(Date, N, Mode):
    '''
    :param Date: Query 的初始日期
    :param N: 需要查询的天数
    :return: Collection, Size_Post, Date_List
    '''
    # 存储分配
    Collection = []
    Size_Post = []
    Date_List = []
    i = 0  # Control Iteration Times
    while i < N:
        Filter_Conf1 = {"crawl_time": {"$regex": r"^.*%s.*$" % Date}, "reply_num": {"$gte": 0},
                       "bright_reply_num": {"$gte": 0}, "browse_num": {"$gte": 0}}
        Filter_Conf2 = {"url": 0, "publish_time": 0}  # 确定需要映射的返回参数
        Get_Object = GetData(Filter_Conf1, Filter_Conf2, Mode)  # 创建GetData实例
        Table, Size = Get_Object.Table, Get_Object.Size  # 通过属性访问
        if Size == 0:
            if i != N:
                print("%s Out Date Index" % Date)
            break
        else:
            print("Is Collecting the %d Day:" % (i+1))
            Collection.append(Table)
            Size_Post.append(Size)
            Date_List.append(Date)
            i = i + 1
        List = Date.split('-')
        List = [int(x) for x in List]  # 字符串转整型变量
        # 天数加一 假定数据中的日期的Value是正确的
        List = date_increase(List)  # 得到数据中日期增加的列表
        for j in range(0, len(List)):
            if j == 0:
                List[j] = str(List[j])
            else:
                if 0 < List[j] < 10:
                    List[j] = str("0%s" % List[j])  # 保证日期的格式的一致性
                else:
                    List[j] = str(List[j])
        Separator = '-'
        List = Separator.join(List)
        Date = List
    return Collection, Size_Post, Date_List




