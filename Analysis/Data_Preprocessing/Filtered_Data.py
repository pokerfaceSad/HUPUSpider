from Data_Preprocessing.Get_Data import get_data
from Data_Preprocessing.Date_Increase import date_increase
import settings


# Filter_Conf1为对Value值的筛选  Filter_Conf2确定了需要映射的数据 设置初始的Filter_Conf
# 对于不同日期的帖子 很难确定回复数 点亮数 浏览数的门限值


def filtered_data():
    # 存储分配
    Collection = []
    Size_Post = []
    Date_List = []
    Stop_Flag = True
    while Stop_Flag:
        Filter_Conf1 = {"crawl_time": {"$regex": r"^.*%s.*$" % settings.Start_Time}, "reply_num": {"$gte": 0},
                       "bright_reply_num": {"$gte": 0}, "browse_num": {"$gte": 0}}
        Filter_Conf2 = {"url": 0, "publish_time": 0, "bright_reply_dict": 0}  # 确定需要映射的返回参数
        Table, Size = get_data(Filter_Conf1, Filter_Conf2)
        if Size == 0:
            print("Collecting Data Over")
            break
        else:
            Collection.append(Table)
            Size_Post.append(Size)
            Date_List.append(settings.Start_Time)
        List = settings.Start_Time.split('-')
        List = [int(x) for x in List]  # 字符串转整型变量
        # 天数加一 假定数据中的日期的Value是正确的
        List = date_increase(List)  # 得到数据中日期增加的列表
        for i in range(0, len(List)):
            if i == 0:
                List[i] = str(List[i])
            else:
                if 0 < List[i] < 10:
                    List[i] = str("0%s" % List[i])  # 保证日期的格式的一致性
                else:
                    List[i] = str(List[i])
        Separator = '-'
        List = Separator.join(List)
        settings.Start_Time = List
    return Collection, Size_Post, Date_List




