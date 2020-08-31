import json

link = '1'
with open('news.json', 'r') as file:
    news_load = json.load(file)

    news_feed = {}
    for news in news_load:
        if news['link'] == int(link):
            news_feed = news

    print(news_feed)