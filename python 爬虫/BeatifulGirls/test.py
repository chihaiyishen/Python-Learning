import requests
from lxml import html
import os
from multiprocessing.dummy import Pool as ThreadPool

def header(referer):
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers

# 获取主页列表
def getPage(pageNum):
    baseUrl = 'http://www.mzitu.com/page/{}'.format(pageNum)
    selector = html.fromstring(requests.get(baseUrl).content)
    urls = []
    for i in selector.xpath('//ul[@id="pins"]/li/a/@href'):
        urls.append(i)
        print(i)
    return urls


# 图片链接列表， 标题
# url是详情页链接
def getPiclink(url):
    sel = html.fromstring(requests.get(url).content)
    # 图片总数
    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
    # 标题
    title = sel.xpath('//h2[@class="main-title"]/text()')[0]
    # 文件夹格式
    dirName = u"【{}P】{}".format(total, title)
    # 新建文件夹
    os.mkdir(dirName)

    n = 1
    for i in range(int(total)):
        # 每一页
        try:
            link = '{}/{}'.format(url, i+1)
            s = html.fromstring(requests.get(link).content)
            # 图片地址在src标签中
            jpgLink = s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
            # print(jpgLink)
            # 文件写入的名称：当前路径／文件夹／文件名
            filename = '%s/%s/%s.jpg' % (os.path.abspath('.'), dirName, n)
            print(u'开始下载图片:%s 第%s张' % (dirName, n))
            with open(filename, "wb+") as jpg:
                jpg.write(requests.get(jpgLink, headers=header(jpgLink)).content)
            n += 1
        except:
            pass


if __name__ == '__main__':
    pageNum = input(u'请输入页码：')
    p = getPage(pageNum)
    with ThreadPool(4) as pool:
        pool.map(getPiclink, p)    