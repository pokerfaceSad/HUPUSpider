from Theme_Analysis.theme_analysis import ThemeAnalysis
import settings

if __name__ == "__main__":
    Date = input("请输入查询日期(需要大于%s):\nDate" % settings.Start_Time)
    N = eval(input("请输入查询天数:\nN"))
    Mode = eval(input("请输入查询模式(1代表先Rank再查询)\nMode"))
    Analysis = ThemeAnalysis(Date, N, Mode)
