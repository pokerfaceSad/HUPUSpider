import numpy as np
import jieba.analyse
from zhon.hanzi import punctuation
from PIL import Image
from wordcloud import WordCloud
from matplotlib import pyplot
import settings
from Data_Preprocessing.Filtered_Data import filtered_data


def word_cloud_generate(Date):

    '''
    :param Date: A str Object in Standard pattern joined with '-'.exp:"2018-11-03"
    :return:A Flag: If Data exits in the Date, return 1; else: return 0
    '''

    Collection, Size_Post, Date_List = filtered_data()
    Title_List = []
    if Date in Date_List:
        k = Date_List.index(Date)
    else:
        return 0
    Weight_List = np.zeros((1, Size_Post[k]))  # 类似于词频的权重数组
    for i in range(0, Size_Post[k]):
        # 去除中文符号
        temp = "".join(jieba.lcut(re.sub(r"([%s])+" % punctuation, "", Collection[k][i]["post_content"]), cut_all=False))
        # 去除帖子中含有的一些标志词： ZT（转贴） ZS（字数） TX等无实际意义的词
        temp = re.sub(r"([Zz][Tt]|[Zz][Ss]|[Tt][Xx]|[Jj][Rr]|[.]{1,6}|\n|[A-Za-z_]+|客户端|"
                      r"视频无法播放浏览器版本过低请升级浏览器或者使用其他浏览器|"
                      r"虎扑步行街|步行街主干道|虎扑|/+|[:]+|由.*[\u4e00-\u9fff]+.*发表在|发自|[0-9]+|由|发表在)", "", temp)
        print(temp)
        # 字典调整 加入有可能成词的中文词和停用词表
        jieba.add_word("锁屏", freq=10)
        jieba.add_word("晒一下", freq=10)
        jieba.analyse.set_stop_words("%sStop_words.txt" % settings.Stop_Words_Path)

        Title_List.append(jieba.analyse.extract_tags(temp, topK=3, withWeight=False, allowPOS=()))
        # 给帖子的点亮数和回复数分配不同的权重（数量级在同一水平）
        Weight_List[0][i] = Collection[k][i]["reply_num"] * 0.1 + Collection[k][i]["bright_reply_num"] * 0.9
    Weight_List = Weight_List/sum((Weight_List[0]))

    #  生成所需要的字典Dict
    Freq_Dict = {}
    for i in range(0, Size_Post[k]):
        for j in range(0, len(Title_List[i])):
            # 同一个title中的三个Top_Words的权重是一样的
            Freq_Dict[Title_List[i][j]] = Weight_List[0][i]

    #  从频率表生成词云
    #  parameter set
    #  注意matplotlib库和PIL库读取图片的差别
    Background_Picture = np.array(Image.open("%sHUPU_image.png" % settings.Mask_Image_Path))
    # Background_Picture_1 = 255 * pyplot.imread('C:/Users/lenovo/Documents/Ground_Picture/HUPU_image.png')
    #  读取的像素值在0-1之间
    # 如果用 pyplot 读取图片，需要乘以255（灰度等级256）
    #  注意图片的画布需要设置为白色 Mask 才能捕捉到形状

    # Q1: 词云的生成中，背景的设置出了问题，无法通过参数生成透明背景图片,即便采用生成透明背景图片 也有白色背景
    # Q2: 给Mask图片加上 Contour的设置 和透明的设置无法同时启用(虽然透明背景本身也无效）
    wc = WordCloud(
        font_path="C:/Windows/Fonts/msyhbd.ttc",  # 字体采用微软雅黑
        prefer_horizontal=0.5,  # 词语水平排版出现的频率
        mask=Background_Picture,  # 设置背景图片
        contour_width=2,  # 给形状周围加粗
        contour_color="red",  # 形状边缘线的颜色设置为红色
        scale=1.5,  # 显示设置为原来画布的1.5倍
        max_words=500,  # 显示的最大的词的个数设置为 500
        background_color="white",  # 背景设置成白色
        collocations=True,  # 包括两个词的搭配
        random_state=100  # 100种配色方案
    )
    wc.generate_from_frequencies(Freq_Dict)
    #  改变字体颜色
    #  Display in PIL way
    img = wc.to_image()
    img.show()
    # save in PIL way
    wc.to_file("%s.tif" % Date_List[k])
    return 1

