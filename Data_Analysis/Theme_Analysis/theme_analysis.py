import re
import numpy as np
import jieba.analyse
from zhon.hanzi import punctuation
from PIL import Image
from wordcloud import WordCloud
#  from matplotlib import pyplot
import settings
from Data_Preprocessing.Filtered_Data import filtered_data


class ThemeAnalysis(object):
    '''
    定义一个Theme_Analysis类来进行文本的分析
    '''
    def __init__(self, query_date, n, mode):
        self.query_start = query_date
        self.query_num = n
        self.Mode = mode
        self.Collection, self.Size_Post, self.Date_List = self.get_origin_data()
        if mode == 1:
            self.Title_List, self.Weights_List = self.process_with_figure()
        else:
            self.Title_List, self.Weights_List = self.process_with_keywords()
        self.Freq_Dict = self.generate_dict()
        self.visualize_cloud()

    def get_origin_data(self):
        Collection, Size_Post, Date_List = filtered_data(self.query_start, self.query_num, self.Mode)
        return Collection, Size_Post, Date_List

    def process_with_figure(self):
        Title_List = []
        Weight_List = []  # 权重 List 初始化
        UID_List = []  # 存储帖子的uid_列表
        for i in range(0, len(self.Size_Post)):  # Date 外循环
            # 权重初始化
            UID_temp = []
            for j in range(0, self.Size_Post[i]):  # 帖子内循环
                BreakFlag = False
                UID_temp.append(self.Collection[i][j]["_id"])
                # 去除中文符号
                temp_str = ""
                if i >= 1:
                    for UID_List_Index in range(0, i):
                        if self.Collection[i][j]["_id"] in UID_List[UID_List_Index]:
                            BreakFlag = True
                if BreakFlag:
                    continue
                for bright_reply_Index in range(0, self.Collection[i][j]["bright_reply_num"]):
                    temp_str = temp_str + \
                               self.Collection[i][j]["bright_reply_dict"]["bright_reply_%d" % (bright_reply_Index + 1)] \
                                   ["reply_content"]  # 索引到该帖子的亮评回复连接到 temp_str 中
                temp = "".join(
                    jieba.lcut(re.sub(r"([%s])+" % punctuation, "", self.Collection[i][j]["post_content"] + temp_str),
                               cut_all=False))
                # 去除帖子中含有的一些标志词： ZT（转贴） ZS（字数） TX等无实际意义的词
                temp = re.sub(r"([Zz][Tt]|[Zz][Ss]|[Tt][Xx]|[Jj][Rr]|[.]{1,6}|\n|[A-Za-z_]+|客户端|"
                              r"视频无法播放浏览器版本过低请升级浏览器或者使用其他浏览器|"
                              r"虎扑步行街|步行街主干道|虎扑|/+|[:]+|由.*[\u4e00-\u9fff]+.*发表在|发自|[0-9]+|由|发表在"
                              r"|.*@[\u4e00-\u9fff]+.*|\r|引用|@|发表的|[+-].+|\[.{2}此贴被[\u4e00-\u9fff]+.{2}在\]|修改"
                              r"|\[|\])", "", temp)
                print(temp)
                # 字典调整 加入有可能成词的中文词和停用词表
                File_Object = open("%s%sFixed_words.txt" % (settings.Project_Path, settings.Fixed_Word_Path), 'r',
                                   encoding='utf-8')
                Lines = File_Object.readlines()
                for Index in range(0, len(Lines)):
                    List = Lines[Index].splitlines()[0].split()
                    jieba.add_word(List[0], freq=int(List[1]))
                File_Object.close()  # 关闭文件
                jieba.analyse.set_stop_words("%s%sStop_words.txt" % (settings.Project_Path, settings.Stop_Words_Path))

                Title_List.append(jieba.analyse.extract_tags(temp, topK=3, withWeight=False, allowPOS=()))
                # 给帖子的点亮数和回复数分配不同的权重（数量级在同一水平）
                Weight_List.append(
                    self.Collection[i][j]["reply_num"] * 0.1 + self.Collection[i][j]["bright_reply_num"] * 0.9)
            UID_List.append(UID_temp)
        Weight_List[:] = list(np.array(Weight_List[:]) / sum(Weight_List[:]))
        return Title_List, Weight_List

    def process_with_keywords(self):
        Title_List = []
        Weight_List = {}  # 权重 List 初始化
        for i in range(0, len(self.Size_Post)):  # Date 外循环
            # 权重初始化
            for j in range(0, self.Size_Post[i]):  # 帖子内循环 如果选定的天数超过一天 对同一个帖子不进行剔除
                # 去除中文符号
                temp_str = ""
                for bright_reply_Index in range(0, self.Collection[i][j]["bright_reply_num"]):
                    temp_str = temp_str + \
                               self.Collection[i][j]["bright_reply_dict"]["bright_reply_%d" % (bright_reply_Index + 1)] \
                                   ["reply_content"]  # 索引到该帖子的亮评回复连接到 temp_str 中
                temp = "".join(
                    jieba.lcut(re.sub(r"([%s])+" % punctuation, "", self.Collection[i][j]["post_content"] + temp_str),
                               cut_all=False))
                # 去除帖子中含有的一些标志词： ZT（转贴） ZS（字数） TX等无实际意义的词
                temp = re.sub(r"([Zz][Tt]|[Zz][Ss]|[Tt][Xx]|[Jj][Rr]|[.]{1,6}|\n|[A-Za-z_]+|客户端|"
                              r"视频无法播放浏览器版本过低请升级浏览器或者使用其他浏览器|"
                              r"虎扑步行街|步行街主干道|虎扑|/+|[:]+|由.*[\u4e00-\u9fff]+.*发表在|发自|[0-9]+|由|发表在"
                              r"|.*@[\u4e00-\u9fff]+.*|\r|引用|@|发表的|此贴|[+-].+|\[.{2}此贴被[\u4e00-\u9fff]+.{2}在\]"
                              r"|修改|\[|\])", "", temp)
                print(temp)
                # 字典调整 加入有可能成词的中文词和停用词表
                File_Object = open("%s%sFixed_words.txt" % (settings.Project_Path, settings.Fixed_Word_Path), 'r',
                                   encoding='utf-8')
                Lines = File_Object.readlines()
                for Index in range(0, len(Lines)):
                    List = Lines[Index].splitlines()[0].split()
                    jieba.add_word(List[0], freq=int(List[1]))
                File_Object.close()  # 关闭文件
                jieba.analyse.set_stop_words("%s%sStop_words.txt" % (settings.Project_Path, settings.Stop_Words_Path))

                Title_List.append(jieba.analyse.extract_tags(temp, topK=10, withWeight=False, allowPOS=()))
            if len(Title_List) > 1:
                count = 0
                for Compare_Index in range(0, len(Title_List)):
                    if len(list(set(Title_List[Compare_Index]) & set(Title_List[i]))) >= \
                            round((len(Title_List[i]) * 0.5)):
                        count = count + 1
                        Weight_List["%d" % Compare_Index] = count
        for keys in Weight_List:
            Weight_List[keys] = Weight_List[keys]/sum(list(Weight_List.values()))  # 权重归一化
        weight_list = list(Weight_List.values())
        Non_zeros_index = [int(x) for x in list(Weight_List.keys())]
        for title_index in range(0, len(Title_List)):
            if title_index in Non_zeros_index:
                continue
            else:
                Title_List[title_index] = [0]
        Temp_List = []
        for title_index in range(0, len(Title_List)):
            if Title_List[title_index] != [0]:
                Temp_List.append(Title_List[title_index])
        return Temp_List, weight_list

    def generate_dict(self):
        Freq_Dict = {}
        count = 0
        for Post_Index in range(0, len(self.Title_List)):
            for Word_Index in range(0, len(self.Title_List[Post_Index])):
                Freq_Dict[self.Title_List[Post_Index][Word_Index]] = self.Weights_List[Post_Index]
                count = count + 1
        return Freq_Dict

    def visualize_cloud(self):
        #  从频率表生成词云
        #  parameter set
        #  注意matplotlib库和PIL库读取图片的差别
        Background_Picture = np.array(Image.open("%s%s虎扑.png"
                                                 % (settings.Project_Path, settings.Mask_Image_Path)))
        # Background_Picture_1 = 255 * pyplot.imread('C:/Users/lenovo/Documents/Ground_Picture/HUPU_image.png')
        #  读取的像素值在0-1之间
        # 如果用 pyplot 读取图片，需要乘以255（灰度等级256）
        #  注意图片的画布需要设置为白色 Mask 才能捕捉到形状

        # Q1: 词云的生成中，背景的设置出了问题，无法通过参数生成透明背景图片,即便采用生成透明背景图片 也有白色背景
        # Q2: 给Mask图片加上 Contour的设置 和透明的设置无法同时启用(虽然透明背景本身也无效）
        wc = WordCloud(
            font_path="%s" % settings.Font_Path,  # 字体采用微软雅黑
            prefer_horizontal=0.5,  # 词语水平排版出现的频率
            mask=Background_Picture,  # 设置背景图片
            # contour_width=2,  # 给形状周围加粗
            # contour_color="red",  # 形状边缘线的颜色设置为红色
            scale=1.5,  # 显示设置为原来画布的1.5倍
            max_words=500,  # 显示的最大的词的个数设置为 500
            background_color="white",  # 背景设置成白色
            collocations=True,  # 包括两个词的搭配
            random_state=100  # 100种配色方案
        )
        wc.generate_from_frequencies(self.Freq_Dict)
        #  改变字体颜色
        #  Display in PIL way
        img = wc.to_image()
        img.show()
        # save in PIL way
        wc.to_file("start at %s in %d Day.tif" % (self.Date_List[0], self.query_num))


if __name__ == "__main__":
    Analysis = ThemeAnalysis("2018-11-04", 1, 0)  # Mode =1 Means Get Rank 前%5的帖子
    # Mode=Others Means Get All the Post
    Analysis.visualize_cloud()


