from Data_Preprocessing.Filtered_Data import filtered_data
import settings


if __name__ == "__main__":
    Date = input("请输入需要查询的初始日期(需要大于%s): Date" % settings.Start_Time)  # 函数需要的参数输入
    N = eval(input("请输入需要查询的天数:N"))  # 转换类型
    Collection, Size_Post, Date_List = filtered_data(Date, N)
