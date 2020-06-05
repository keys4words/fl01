from flask import Blueprint, current_app, render_template

from webapp.weather import weather_by_city
from webapp.news.models import News

blueprint = Blueprint('news', __name__)

@blueprint.route('/')
def index():
    page_title = 'My weather forecast'
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    news_list = News.query.order_by(News.published.desc()).all()
    #news_list = get_python_news()
    return render_template('news/index.html', page_title=page_title, weather=weather, news_list=news_list)