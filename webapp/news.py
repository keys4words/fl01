from datetime import datetime
import requests

from bs4 import BeautifulSoup

from webapp.db import db
from webapp.news.models import News

def get_html(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.text
    except(requests.RequestException, ValueError):
        print('Network error')
        return False

def get_python_news():
    html = get_html('https://www.python.org/blogs/')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        # res = []
        for news_item in all_news:
            title = news_item.find('a').text
            url = news_item.find('a')['href']
            published = news_item.find('time')['datetime']
            try:
                published = datetime.strptime(published, '%Y-%m-%d')
            except ValueError:
                published = datetime.now()

            # res.append({
            #     'title': title,
            #     'url': url,
            #     'published': published
            # })
            save_news(title, url, published)
        #return res
        

def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    print(news_exists)
    if not news_exists:
        news_item = News(title=title, url=url, published=published)
        db.session.add(news_item)
        db.session.commit()
    
    
