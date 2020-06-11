from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale
import platform

from webapp.db import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news


if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')

DECLENSIONS = {
    'ря':'рь',
    'та':'т',
    'ля':'ль',
    'ая':'ай',
    'ня':'нь'
}


def remove_declension(month):
    end = DECLENSIONS.get(month[-2:], month[-2:])
    return month[:-2] + end


def validate_date(dt):
    dt = dt.split(' ')
    if len(dt[0]) == 1:
        dt[0] = '0' + dt[0]
    dt[1] = dt[1].capitalize()
    dt[1] = remove_declension(dt[1])
    return ' '.join(dt)


def parse_habr_date(date_str):
    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    
    date_str = validate_date(date_str)
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()

def get_habr_snippets():
    html = get_html('https://habr.com/ru/search/?target_type=posts&q=python&order_by=date')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='content-list_posts').findAll('li', class_='content-list__item_post')
        for news_item in all_news:
            title = news_item.find('a', class_='post__title_link').text
            url = news_item.find('a', class_='post__title_link')['href']
            published = news_item.find('span', class_='post__time').text
            published = parse_habr_date(published)
            #print(title, url, published)
            save_news(title, url, published)


def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_text = soup.find('div', class_='post__text-html').decode_contents()
            if news_text:
                news.text = news_text
                db.session.add(news)
                db.session.commit()