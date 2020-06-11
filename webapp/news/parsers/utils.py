import requests

from webapp.db import db
from webapp.news.models import News


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
           'accept': '*/*'}

def get_html(url):
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        return res.text
    except(requests.RequestException, ValueError):
        print('Network error')
        return False

def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    # print(news_exists)
    if not news_exists:
        news_item = News(title=title, url=url, published=published)
        db.session.add(news_item)
        db.session.commit()
    
    
