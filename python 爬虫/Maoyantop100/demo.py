import requests
import re
import json
from requests.exceptions import RequestException
from multiprocessing import Pool

def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        reponse = requests.get(url, headers=headers)
        if reponse.status_code == 200:
            return reponse.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?<a.*?title="(.*?)".*?>'
                         '.*?<img.*?data-src="(.*?)".*?>'
                         '.*?releasetime">(.*?)</p>'
                         '.*?integer">(.*?)</i>'
                         '.*?fraction">(.*?)</i>.*?</dd>', re.S)

    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'title': item[1],
            'src': item[2],
            'time': item[3].strip()[5:],
            'socre': item[4]+item[5]
        }

def write_to_file(content):
    with open('result2.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/7?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])


