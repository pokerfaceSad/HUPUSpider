from Theme_Analysis.theme_analysis import ThemeAnalysis
from Theme_Analysis.visualization import WordCloudGenerater
import settings

if __name__ == "__main__":
    Date = input("请输入查询日期(需要大于%s):\n" % settings.Start_Time)
    N = eval(input("请输入查询天数:\n"))
    Mode = eval(input("请输入查询模式(1代表查询时Rank)\n"))
    Analysis = ThemeAnalysis(Date, N, Mode)
    Output = WordCloudGenerater(Analysis.freq_dict, Analysis.date_list, Analysis.query_num)
