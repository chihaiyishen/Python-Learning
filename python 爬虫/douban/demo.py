import requests
from urllib.parse import urlencode
import re
import csv
import time

# 获取网页请求数据
def get_one(num):
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 66.0.3359.170Safari / 537.36'
    }
    params = {
        'start': str(num),
        'limit': '20',
        'sort': 'new_score',
        'status': 'P',
        'percent_type': ''
    }
    base_url = 'https://movie.douban.com/subject/27113517/comments?'
    url = base_url + urlencode(params)
    print("正在采集：" + url)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
    except EOFError as e:
        print(e)
        return None

# 解析网页结构
def parse_page(html):
    info = []
    patten1 = re.compile(r'<div class="comment">.*?<a href=.*?class="">(.*?)</a>.*?<span class="comment-time " title="(.*?)">.*?</span>.*?<p class="">(.*?)</p>.*?</div>', re.S)
    datas = re.findall(patten1, html)
    for data in datas:
        comic = {}
        comic['User'] = data[0].strip()
        comic['Time'] = data[1].strip()
        comic['Comment'] = data[2].strip().split()
        info.append(comic)
    return info

# 保存数据
def write_to_file(info):
    with open('《铁血观音》影评.csv', 'a', newline='') as f:
        fieldnames = ['User', 'Time', 'Comment']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        try:
            writer.writerows(info)
        except:
            pass

# 执行函数
def main():
    for i in range(10):
        html = get_one(i*20)
        datas = parse_page(html)
        write_to_file(datas)
        print('本页采集完毕。')  # 采集完一页后的标识
        time.sleep(1)  # 采集完一页休息一秒

if __name__ == '__main__':
    main()

