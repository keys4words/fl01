from flask import Flask, render_template

from weather import weather_by_city
from news import get_python_news

app = Flask(__name__)

@app.route('/')
def index():
    page_title = 'My weather forecast'
    weather = weather_by_city("Moscow,Russia")
    news_list = get_python_news()
    return render_template('index.html', page_title=page_title, weather=weather, news_list=news_list)

if __name__ == '__main__':
    app.run(debug=True)
