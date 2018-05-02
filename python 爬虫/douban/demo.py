import re
import requests


def page_one(url):

    try:
        reponse = requests.get(url)
        if reponse.status_code == 200:
            return reponse.text
    except requests.ConnectionError:
        return "爬取失败"

def parse_detial(html):
    patten = re.compile('<div.*?comments".*?comment-item".*?<p class="">([\s\S]*?)</p>.*?</div>', re.S)
    results = re.findall(patten, html)
    for result in results:
        yield {
            'fileReview': result
        }

def main():
    target = 'https://movie.douban.com/subject/26683723/comments?start=p'
    supple_url = 'https://movie.douban.com/subject/26683723/comments'
    login_url = 'https://accounts.douban.com/login'
    sum_pattern = ''
    url = "https://movie.douban.com/subject/26683723/comments?start=0&limit=20&sort=new_score&status=P&percent_type="
    html = page_one(url)
    for review in parse_detial(html):
        print(review)


if __name__ == '__main__':
    main()