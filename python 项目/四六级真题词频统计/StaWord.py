import re
import io
import os
from matplotlib import pyplot as plt


#  画图
def draw(data, num):
    # 单词数据
    data1 = data[:num]
    # 循环遍历
    for word in data1:
        # 获取单词数据
        plt.bar(word[:1], word[-1:])

    plt.legend()
    # 画 x 轴
    plt.xlabel('words')
    # 画 y 轴
    plt.ylabel('rate')
    # 画标题
    plt.title('46 level high frequency words')
    plt.show()

# 输出
def input(file_path, data):
    with io.open(file_path, 'w', encoding='utf-8') as f:
        for i in data:
            f.write(str(i))
            f.write('\n')

# 词频统计
def comm(path):
    # 表示当前所处的文件夹的绝对路径
    path1 = os.path.abspath('.')
    # 输出路径
    out_path2 = path + '\\3\\' + '2' + '.txt'
    num = 1
    # 文本输出路径
    txt_path = path + '\\2\\'
    # 当前路径下的所有文件
    files = os.listdir(txt_path)
    # 创建空的字典
    test1 = dict()
    for f in files:
        # 要处理的文件路径
        file_path = txt_path + f
        with io.open(file_path, 'r') as f1:
            data = f1.read()
            # 匹配所有字母，不区分大小写
            words = [s.lower() for s in re.findall('[a-zA-Z]+', data)]
            # 过滤的单词
            badwords = ['the', 'and', 'that', 'are', 'for']
            for word in words:
                # 过滤的条件
                if len(word) > 2 and word not in badwords:
                    test1[word] = test1.get(word, 0) + 1

    # 排序字典，从高到低输出，得到新的列表
    test2 = sorted(test1.items(), key=lambda x: x[1], reverse=True).copy()
    # 输出词频 txt 文本
    input(out_path2, test2)
    # 画图表
    draw(test2, 10)

