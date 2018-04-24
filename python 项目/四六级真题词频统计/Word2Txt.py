from win32com import client as wc
import os

path1 = os.path.abspath('.')  # 表示当前所处的文件夹的绝对路径
all_FileNum = 1

# 关闭 WPS 软件
def closesoft():
    print('''''挂载程序关闭中…… 

          ''')
    import win32com
    import win32com.client
    wc = win32com.client.constants

    try:
        wps = win32com.client.gencache.EnsureDispatch('kwps.application')
    except:
        wps = win32com.client.gencache.EnsureDispatch('wps.application')
    else:
        wps = win32com.client.gencache.EnsureDispatch('word.application')
    try:
        wps.Documents.Close()
        wps.Documents.Close(wc.wdDoNotSaveChanges)
        wps.Quit
    except:
        pass

# 转换 word 文档成 txt 文档
def Translate(path):
    # 文本数
    global all_FileNum
    # word 文件夹路径
    doc_path = path + '\\1\\'
    # 输出 txt 文件夹路径
    txt_path = path + '\\2\\'
    # 获取 word 文件夹下所有的文件
    files = os.listdir(doc_path)
    # 遍历文件
    for f in files:
        # 得到 word 文档后缀名
        if (f[0] == '~' or f[0] == '.'):
           continue
        # 要处理的文件名
        new = doc_path + f
        print('word2txt...' + str(all_FileNum))
        # 新的文件名
        tmp = txt_path + str(all_FileNum)
        word = wc.Dispatch('Word.Application')
        # 打开 word 文件
        doc = word.Documents.Open(new)
        # 保存新的 txt 文件
        doc.SaveAs(tmp + '.txt', 4)
        all_FileNum = all_FileNum + 1
    doc.Close()
    word.Quit()

