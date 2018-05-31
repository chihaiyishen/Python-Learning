from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
import csv

browser = webdriver.PhantomJS()

# 请求页面
def get_one(url):
    print('正在爬取中...')
    try:
        browser.get(url)
        html = browser.page_source
        # get_datas(html)
        return html
    except selenium.common.exceptions.TimeoutException:
        # 遇到请求超时异常，重新在请求
        return None

# 解析页面
def parse_one(html):
    soup = BeautifulSoup(html, 'lxml')
    name = soup.select('div.listing_info > div.listing_title > a')
    city = soup.select('div.listing_info > div.listing_title > span')
    rank = soup.select(' div.listing_info > div.listing_rating > div:nth-of-type(3) > span')
    img = soup.select('img[width="180"]')
    info = []
    for name, city, rank, img in zip(name, city, rank, img):
        c = city.get_text()
        c1 = c.replace('(', '')
        c2 = c1.replace(')', '')
        data = {}
        data['Name'] = name.get_text()
        data['City'] = c2
        data['Rank'] = rank.get_text()
        data['Img'] = img.get('src')
        info.append(data)
        print(data)
    print('爬取成功')
    return info

# 保存数据
def write_to_file(info):
    print('正在写入文件')
    with open('日本著名景点.csv', 'a', newline='') as f:
        fieldnames = ['Name', 'City', 'Rank', 'Img']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(info)
        print('写入成功')

def main():
    url = 'https://www.tripadvisor.cn/Attractions-g294232-Activities-Japan.html'
    html = get_one(url)
    data = parse_one(html)
    write_to_file(data)

if __name__ == '__main__':
    main()
