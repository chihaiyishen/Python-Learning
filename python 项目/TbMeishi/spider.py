import re
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *
import pymongo

# 定义 mongo 链接变量
clinet = pymongo.MongoClient(MONGO_URL)
# 定义 mongo 数据库变量
db = clinet[MONGO_DB]

# 定义浏览器驱动
# browser = webdriver.Chrome()
# 无界面浏览器
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# 设置网站等待时间
wait = WebDriverWait(browser, 10)

# 设置窗口大小
browser.set_window_size(1400, 900)

# 定义搜索函数
def search():
    print('正在搜索')
    try:
        # 要请求的目标地址
        browser.get('https://www.taobao.com')
        # 获取淘宝首页的输入框
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        # 获取淘宝页面的搜素按钮
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        # 在输入框中输入内容
        input.send_keys('美食')
        # 点击按钮提交
        submit.click()
        # 获取搜素页数
        total = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )
        # 调用加载信息函数
        get_products()
        # 返回搜索页数结果
        return total.text
    except selenium.common.exceptions.TimeoutException:
        # 遇到请求超时异常，重新在请求
        return search()

def next_page(page_number):
    print('正在翻页', page_number)
    try:
        # 获取淘宝页码的输入框
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        # 获取淘宝页码的确定按钮
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        # 清空原本输入框的内容
        input.clear()
        # 向输入框填入页数
        input.send_keys(page_number)
        # 点击按钮
        submit.click()
        # 判断当前的搜索页面是否于当前的页面相同
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number))
        )
        # 调用加载信息函数
        get_products()
    except selenium.common.exceptions.TimeoutException:
        # 遇到请求超时异常，重新递归请求
        next_page(page_number)


def get_products():
    # 加载所有宝贝信息
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    # 获取整个网页源代码
    html = browser.page_source
    # 使用 pyquery 解析源代码
    doc = pq(html)
    # 选择所有的 items
    items = doc('#mainsrp-itemlist .items .item').items()
    # 循环遍历所有的 items
    for item in items:
        # 重新构建我们想要的信息字典
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_monogo(product)

def save_to_monogo(result):
    try:
        # 判断保存是否成功
        if db[MONGO_TABLE].insert(result):
            # 保存成功输入相应信息
            print('存储到 MONGODB 成功', result)
    except Exception:
        # 保存失败输出相应信息
        print('存储到 MONGODB 失败', result)

def main():
    # 测试
    total = search()
    # 使用正则表达式获取页数
    total = int(re.compile('(\d+)').search(total).group(1))
    # 循环遍历页数
    for i in range(2, total + 1):
        # 循环翻页
        next_page(i)
    # 执行完成关闭浏览器
    browser.close()

if __name__ == '__main__':
    main()