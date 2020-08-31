from collections import defaultdict
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from django.template import RequestContext
import json
import os
import datetime
import random


# Create your views here.
def home(request):
    # return HttpResponse('Coming soon')
    return redirect('/news')


class MainPage(View):
    def get(self, request):
        q = request.GET.get('q')
        news_feed = []
        with open(settings.NEWS_JSON_PATH, 'r') as file:
            news_load = json.load(file)
        for news in news_load:
            news['created'] = datetime.datetime.strptime(news['created'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            news['created'] = datetime.datetime.strptime(news['created'], "%Y-%m-%d")
            if q != None and news['title'].find(q) != -1:
                news_feed.append(news)
            if q == None:
                news_feed = news_load
        return render(request, "news/main_page.html", context={'news_load': news_feed})



class NewsView(View):
    def get(self, request, link):
        news_load = my_news()
        news_feed = {}
        for news in news_load:
            if news['link'] == int(link):
                news_feed = news

        return render(request, 'news/index.html', news_feed)

def my_news():
    with open(settings.NEWS_JSON_PATH, 'r') as file:
        news_load = json.load(file)

    return news_load

class Create_Page(View):
    def post(self, request, *args, **kwargs):
        exist_news = my_news()

        title = request.POST.get('title')
        text = request.POST.get('text')
        link = len(exist_news) + 1
        created = datetime.datetime.now()
        created= created.strftime("%Y-%m-%d %H:%M:%S")

        dic = {}
        dic["title"] = title
        dic['text'] = text
        dic['link'] = link
        dic['created'] = created

        exist_news.append(dic)
        with open(settings.NEWS_JSON_PATH, 'w') as file:
            json.dump(exist_news, file)
        return redirect('/news')

    def get(self, request):
        return render(request, 'news/create_page.html')