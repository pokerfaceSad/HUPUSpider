from Theme_Analysis.theme_analysis import ThemeAnalysis
from Theme_Analysis.visualization import WordCloudGenerater
import time
import settings

if __name__ == "__main__":
    generate = {}
while True:
    while True:
        Date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        print(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))
        if time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time())) == (Date + "-23-59"):
            Analysis_bxj = ThemeAnalysis(Date, 1, 1)
            Output = WordCloudGenerater(Analysis_bxj.freq_dict, Analysis_bxj.date_list, Analysis_bxj.query_num)
            settings.Collection_Name = "VOTE_COL"
            settings.Rank_Post = 0.10
            Analysis_basket = ThemeAnalysis(Date, 1, 1)
            Output_basket = WordCloudGenerater(Analysis_basket.freq_dict, Analysis_basket.date_list,
                                               Analysis_basket.query_num)
            settings.Collection_Name = "BXJ_COL"
            time.sleep(30)
        else:
            time.sleep(30)  # 等待30s
