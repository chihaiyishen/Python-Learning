#读取docx中的文本代码示例
import sys, os
import Word2Txt
import StaWord

# 表示当前所处的文件夹的绝对路径
path1 = os.path.abspath('.')

def run():
    # word 文档转 txt 文档
    Word2Txt.closesoft()
    Word2Txt.Translate(path1)

    # 输出词频
    StaWord.comm(path1)

if __name__ == '__main__':
    run()



