from wordcloud import WordCloud
import settings
# from PIL import Image
# from matplotlib import pyplot


class WordCloudGenerater(object):
    def __init__(self, dict, date_list, n):
        self.freq_dict = dict
        self.date_list = date_list
        self.query_num = n
        self.visualizae_cloud()

    def visualizae_cloud(self):
        #  从频率表生成词云
        #  parameter set
        #  注意matplotlib库和PIL库读取图片的差别
        # Background_Picture = np.array(Image.open("%s%s虎扑.png"
        #                                          % (settings.Project_Path, settings.Mask_Image_Path)))
        # Background_Picture_1 = 255 * pyplot.imread('C:/Users/lenovo/Documents/Ground_Picture/HUPU_image.png')
        #  读取的像素值在0-1之间
        # 如果用 pyplot 读取图片，需要乘以255（灰度等级256）
        #  注意图片的画布需要设置为白色 Mask 才能捕捉到形状
        #  wordcloud中有默认的停用词表不会显示

        # Q1: 词云的生成中，背景的设置出了问题，无法通过参数生成透明背景图片,即便采用生成透明背景图片 也有白色背景
        # Q2: 给Mask图片加上 Contour的设置 和透明的设置无法同时启用(虽然透明背景本身也无效）
        print("Start Generate WordCloud:")
        # 依据Dict的大小动态调整词云的大小
        # 300词设置图片初始大小1200*600
        wc = WordCloud(
            font_path = settings.Project_Path + "Fonts/" + settings.Font_Path,  # 字体采用微软雅黑
            prefer_horizontal=0.5,  # 词语水平排版出现的频率
            width=round(len(self.freq_dict) / 300 * 1200),  # 设置图片大小
            height=round(len(self.freq_dict) / 300 * 600),
            # mask=Background_Picture,  # 设置背景图片
            # contour_width=2,  # 给形状周围加粗
            # contour_color="red",  # 形状边缘线的颜色设置为红色
            # scale=1,  # 显示设置为原来画布的3倍 针对于Mask_Image有效
            max_words=500,  # 显示的最大的词的个数设置为 500
            background_color="black",  # 背景设置成白色
            random_state=100,  # 100种配色方案
            min_font_size=8,  # 设置最小的字体大小
            max_font_size=50  # 设置最大的字体大小
        )
        wc.generate_from_frequencies(self.freq_dict)
        #  改变字体颜色
        #  Display in PIL way
        img = wc.to_image()
        img.show()
        # save in PIL way
        wc.to_file("start at %s in %d Day.tif" % (self.date_list[0], self.query_num))
        print("Generate WordCloud Over.")
