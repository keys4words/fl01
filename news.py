import requests
from bs4 import BeautifulSoup

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
        res = []
        for news_item in all_news:
            title = news_item.find('a').text
            url = news_item.find('a')['href']
            published = news_item.find('time').text
            res.append({
                'title': title,
                'url': url,
                'published': published
            })
        return res
    return False
    
