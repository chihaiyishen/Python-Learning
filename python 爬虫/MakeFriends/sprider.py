import requests
import xlwt
import xlsxwriter
import os
from hashlib import md5
from urllib.parse import urlencode
from config import *
import pymongo

# 定义 mongo 链接变量
clinet = pymongo.MongoClient(MONGO_URL)
# 定义 mongo 数据库变量
db = clinet[MONGO_DB]

'''
解析网站
'''
def get_one(page, startage, endage, gender, startheight, endheight, salary):
    # 设置请求头
    headers = {
        'Referer': 'http://www.lovewzly.com/jiaoyou.html',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 66.0.3359.170Safari / 537.36'
    }

    # 设置请求参数
    params = {
        # 页数
        'page':page,
        # 起始年龄
        'startage': startage,
        # 截止年龄
        'endage':endage,
        # 性别
        'gender':gender,
        # 所在城市的编号
        'cityid':'52',
        # 起始身高
        'startheight':startheight,
        # 终止身高
        'endheight':endheight,
        # 是否结婚
        'marry':'1',
        # 教育水平
        'educatin':'40',
        # 工资薪水
        'salary':salary
    }

    # 网站链接
    base_url = 'http://www.lovewzly.com/api/user/pc/list/search?'
    # 拼接请求参数
    url = base_url + urlencode(params)
    # 调试信息
    print(url)
    while True:
        try:
            # 利用 requests 库请求目标地址
            response = requests.get(url, headers=headers)
            # 判断请求的结果是否有效
            if response.status_code == 200:
                # 返回 json 数据
                return response.json()
        except ConnectionError:
            return None

'''
设置年龄
'''
def query_age():
    # 终端输入年龄
    age = input('请输入期望对方年龄(如:20)：')
    # 年龄区间进行判断
    if 21 <= int(age) <= 30:
        startage = 21
        endage = 30
    elif 31 <= int(age) <= 40:
        startage = 31
        endage = 40
    elif 41 <= int(age) <= 50:
        startage = 41
        endage = 50
    else:
        startage = 0
        endage = 0
    # 返回起始年龄和终止年龄
    return startage, endage

'''
设置性别参数
'''
def query_sex():
    '''性别筛选'''
    # 终端性别字符串的输入
    sex = input('请输入期望对方性别(如:女):')
    # 对输入的信息进行判断
    if sex == '男':
       gender = 1
    else:
       gender = 2

    # 返回性别对应的数字
    return gender
'''
设置身高参数
'''
def query_height():
    '''身高筛选'''
    # 终端输入身高信息
    height = input('请输入期望对方身高(如:162):')
    # 身高区域进行判断
    if 151 <= int(height) <= 160:
        startheight = 151
        endheight = 160
    elif 161 <= int(height) <= 170:
        startheight = 161
        endheight = 170
    elif 171 <= int(height) <= 180:
        startheight = 171
        endheight = 180
    elif 181 <= int(height) <= 190:
        startheight = 181
        endheight = 190
    else:
        startheight = 0
        endheight = 0

    # 返回对应的起始身高和终止身高
    return startheight, endheight

'''
设置薪水参数
'''
def query_money():
    '''待遇筛选'''
    # 终端输入薪水区间
    money = input('请输入期望的对方月薪(如:8000):')

    # 薪水区间进行判断
    if 2000 <= int(money) < 5000:
        salary = 2
    elif 5000 <= int(money) < 10000:
        salary = 3
    elif 10000 <= int(money) <= 20000:
        salary = 4
    elif 20000 <= int(money):
        salary = 5
    else:
        salary = 0
    # 返回薪水参数
    return salary

'''
查询符合条件的数据
'''
def query_data():
    print('请输入你的筛选条件, 开始本次姻缘')
    # 获取终端输入的性别
    gender = query_sex()
    # 获取终端输入的起始身高和终止身高
    startheight, endheight = query_height()
    # 获取终端输入的开始年龄和终止年龄
    startage, endage = query_age()
    # 获取终端输入的薪水
    salary = query_money()
    # 循环遍历 10 次，即抓取 10 次页面的数据
    for i in range(1, 10):
        # 获取抓取到的 json 数据
        json = get_one(i, startage, endage, gender, startheight, endheight, salary)
        # 循环遍历每个 json 数据
        for item in get_person(json):
            # 保存到 monogo 数据库
            save_to_monogo(item)
            # 保存图片
            save_image(item)
'''
图片保存
'''
def save_image(item):
    # 判断当前目录是否存在 images2 文件夹
    if not os.path.exists('images2'):
        # 创建 images2 文件夹
        os.mkdir('images2')
    try:
        # 获得 image 信息
        image_url = item.get('avatar')
        # 利用 requests 请求图片地址
        response = requests.get(image_url)
        # 判断请求的地址是否有效
        if response.status_code == 200:
            # 设置图片保存地址
            file_path = '{0}/{1}.{2}'.format('images2', md5(response.content).hexdigest(), 'jpg')
            # 判断文件是否已经存在
            if not os.path.exists(file_path):
                # 打开对应的文件
                with open(file_path, 'wb')as f:
                    # 保存图片信息
                    f.write(response.content)
            else:
                # 输出图片保存成功信息
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        # 输出图片保存失败信息
        print('Failed to save image')

'''
保存数据到 monogo 数据库
'''
def save_to_monogo(result):
    try:
        # 判断保存是否成功
        if db[MONGO_TABLE].insert(result):
            # 保存成功输入相应信息
            print('存储到 MONGODB 成功', result)
    except Exception:
        # 保存失败输出相应信息
        print('存储到 MONGODB 失败', result)

# 解析数据
def get_person(json):
    # 判断 json 是否为空
    if json:
        # 获取 data 数据
        data = json.get('data').get('list')
    else:
        # 输出错误信息
        print('没有符合你的条件')
    if data:
        # 循环遍历 data 数据，重新构造新的字典
        for person in data:
            yield {
                # 用户 id
                'userid':person.get('userid'),
                # 用户名
                'username': person.get('username'),
                # 性别
                'gender': person.get('gender'),
                # 出现日期
                'birthdayyear': person.get('birthdayyear'),
                # 身高
                'height': person.get('height'),
                # 省份
                'province': person.get('province'),
                # 教育程度
                'education': person.get('education'),
                # 签名
                'monolog': person.get('monolog'),
                # 图片
                'avatar':person.get('avatar')
            }

def main():
    query_data()

if __name__ == '__main__':
    main()