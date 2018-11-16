import re
import numpy as np
import jieba.analyse
import settings
from Data_Preprocessing.Filtered_Data import filtered_data


class ThemeAnalysis(object):
    '''
    定义一个Theme_Analysis类来进行文本的分析
    '''
    def __init__(self, query_date, n, mode):
        self.query_start = query_date
        self.query_num = n
        self.mode = mode
        self.collection, self.size_Post, self.date_list = self.get_origin_data()
        self.title_list, self.weights_list, self.temp_num_list = self.process_with_figure()
        self.freq_dict = self.generate_dict()

    def get_origin_data(self):
        collection, size_post, date_list = filtered_data(self.query_start, self.query_num, self.mode)
        return collection, size_post, date_list

    def process_with_figure(self):
        # 预先进行字典调整 加入有可能成词的中文词和停用词表
        file_object = open("%s%sFixed_words.txt" % (settings.Project_Path, settings.Fixed_Word_Path), 'r',
                           encoding='utf-8')
        lines = file_object.readlines()
        for Index in range(0, len(lines)):
            word_list = lines[Index].splitlines()[0].split()
            jieba.add_word(word_list[0], freq=int(word_list[1]))
        file_object.close()  # 关闭文件
        title_list = []
        weight_list = []  # 权重 List 初始化
        temp_num_bright = []
        uid_list = []  # 存储帖子的uid_列表
        print("Start Data Process:")
        for i in range(0, len(self.size_Post)):  # Date 外循环
            print("Start Processing the %d Day:" % (i+1))
            # 权重初始化
            uid_temp = []
            temp_num_list = []
            for j in range(0, self.size_Post[i]):  # 帖子内循环
                print("Start Processing the %d hot Post:" % (j+1))
                temp_num = 0
                break_flag = False
                uid_temp.append(self.collection[i][j]["_id"])
                # 去除中文符号
                temp_str = ""
                if i >= 1:
                    for UID_List_Index in range(0, i):
                        if self.collection[i][j]["_id"] in uid_list[UID_List_Index]:
                            break_flag = True
                if break_flag:
                    continue
                for bright_reply_Index in range(0, self.collection[i][j]["bright_reply_num"]):
                    temp_str = temp_str + \
                               self.collection[i][j]["bright_reply_dict"]["bright_reply_%d" % (bright_reply_Index + 1)]\
                                   ["reply_content"]  # 索引到该帖子的亮评回复连接到 temp_str 中
                    temp_num = temp_num + int(self.collection[i][j]["bright_reply_dict"]["bright_reply_%d" %
                                                                    (bright_reply_Index + 1)]["bright_num"])
                # 替换一些无意义的符号 正则表达式最好是分开来写 避免耗时太长的问题
                temp = "".join(
                    jieba.lcut(re.sub(r"([【】&*￥#$~-——/<>=%_(:3」∠)_❤\+\-\[\].·]+)", "",
                                      self.collection[i][j]["post_content"]
                                      + temp_str), cut_all=False))
                #  去除帖子中的一些 ZT，ZS，TX, JR LZ \n\r\f\v等无意义的字符
                temp = re.sub(r"([Zz][Tt]|[Zz][Ss]|[Tt][Xx]|[Jj][Rr]|[Ll][Zz]|[Mm][Jj]|[\s]{1,3})", "", temp)
                #  去除帖子中包含的网址 由***发表在虎扑步行街**等无意义的句子 非贪心匹配
                #  [\u4e00-\u9fa5]用来匹配汉字
                temp = re.sub(r"(由([\u4e00-\u9fa5]|[A-Za-z0-9])+?发表在虎扑步行街.+?com.{1,5})", "", temp)
                temp = re.sub(r"(由([\u4e00-\u9fa5]|[A-Za-z0-9])+?发表在虎扑篮球湿乎乎的话题.+?vote)", "", temp)
                # print(temp)
                temp = re.sub(r"(无法播放，浏览器版本过低，请升级浏览器或者使用其他浏览器)", "", temp)
                temp = re.sub(r"(发自虎扑[A-Za-z]+?客户端)", "", temp)
                temp = re.sub(r"(发自手机虎扑.+?com)", "", temp)
                temp = re.sub(r"(引用@([\u4e00-\u9fa5]|[A-Za-z0-9])+?发表的)", "", temp)
                temp = re.sub(r"(此帖被([\u4e00-\u9fa5]|[A-Za-z0-9])+?在[0-9]+?修改)", "", temp)
                temp = re.sub(r"(由([\u4e00-\u9fa5]|[A-Za-z0-9])+?发表在虎扑篮球路人王专区.+?lurenwang)", "", temp)
                temp = re.sub(r"([0-9]+(年|月|日|万|个|千|岁))", "", temp)
                temp = re.sub(r"https[A-Za-z0-9]+", "", temp)
                # 去除帖子中的数字
                temp = re.sub(r"[0-9]+?", "", temp)
                # 去除帖子中出现的长链接等不明字符串
                temp = re.sub(r"[A-za-z?]{30,100}", "", temp)
                # print(temp)
                print("Start Get KeyWords:")
                jieba.analyse.set_stop_words("%s%sStop_words.txt" % (settings.Project_Path, settings.Stop_Words_Path))
                title_list.append(jieba.analyse.extract_tags(temp, topK=3, withWeight=False, allowPOS=()))
                print("Get Words Over.")
                # 给帖子的点亮数和回复数分配不同的权重（数量级在同一水平）
                # 权重调整
                weight_list.append(
                    self.collection[i][j]["reply_num"] * 0.001 + self.collection[i][j]["bright_reply_num"] * 0.4995 +
                    temp_num / self.collection[i][j]["bright_reply_num"] * 0.4995)
                temp_num_list.append(temp_num / self.collection[i][j]["bright_reply_num"])
            uid_list.append(uid_temp)
            print("Process the %d Day Over." % (i+1))
            temp_num_bright.append(temp_num_list)
        weight_list[:] = list(np.array(weight_list[:]) / sum(weight_list[:]))
        print("Process the Data Over.")
        return title_list, weight_list, temp_num_bright

    def generate_dict(self):
        freq_dict = {}
        count = 0
        print("Start Generate Freq_Dict:")
        for post_index in range(0, len(self.title_list)):
            for word_index in range(0, len(self.title_list[post_index])):
                breakflag = False
                if self.title_list[post_index][word_index].upper() in [key.lower for key in list(freq_dict.keys())]:
                    #  如果不同的帖子之间的关键词有重复的 将两个帖子的权重相加
                    freq_dict["%s" % self.title_list[post_index][word_index]] = \
                        freq_dict["%s" % self.title_list[post_index][word_index]] + self.weights_list[post_index]
                    continue
                for keyvalue in list(freq_dict.keys()):
                    if self.title_list[post_index][word_index].lower() in keyvalue.lower():
                        breakflag = True
                        break
                    if keyvalue.lower() in self.title_list[post_index][word_index].lower():
                        breakflag = True
                        break
                if breakflag:
                    continue
                freq_dict[self.title_list[post_index][word_index]] = self.weights_list[post_index]
                count = count + 1
        print("Generate Freq_Dict Over.")
        return freq_dict



