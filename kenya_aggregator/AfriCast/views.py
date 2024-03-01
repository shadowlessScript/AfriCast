from django.shortcuts import render
from .news_crawler import start_crawler, article_list
from .category_crawler import start_category_crawler, cat_article_list

# Create your views here.
def index(request):
    start_crawler()

    articles = article_list[:]
    article_list.clear()
    return render(request, "base.html",{"articles": articles })


def business(request, category):
    start_category_crawler(category)

    articles = cat_article_list[:]
    cat_article_list.clear()
    return render(request, "base.html", {"articles": articles})