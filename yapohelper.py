# -*- coding:utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup

from yapostatements import *

BASE_URI = "http://www3.nhk.or.jp/news/"
BASE_ENCODING = 'utf-8'
ENDPOINT = {
    "TOP_NEWS"     : "easy/top-list.json",
    "NEWS_LIST"    : "easy/news-list.json",
    "KOYOMI"       : "json/koyomi.json",
    "REIKAI"       : "easy/{news_id}/{news_id}.out.dic",
    "NEWS_ARTICLE" : "easy/{news_id}/{news_id}.html"
}
MAIN_DIV_WRAPPER = "newsarticle"
PATTERN = r'\((\w+):(\w+)\)'
ID_PATTERN = r"http:\/\/www3\.nhk\.or\.jp\/news\/easy\/(k[0-9]{14})+\/k[0-9]{14}\.html"
TEST_URI = "http://www3.nhk.or.jp/news/easy/k10014977351000/k10014977351000.html"


def make_article_url(news_id, endpoint="NEWS_ARTICLE"):
    """
    Return url.
    """
    return BASE_URI + ENDPOINT[endpoint].format(news_id=news_id)


def get_article_vocab(preprocessed_string, vocab_dictionary):
    """
    Parse per article.
    Make word + reading vocabulary list.
    """
    matches = re.findall(PATTERN, preprocessed_string)
    for word, reading in matches:
        vocab_dictionary[word] = reading


def get_article_raw(preprocessed_string):
    """
    Return article's raw text without kanji's reading.
    """
    return re.sub(PATTERN, r'\1', preprocessed_string).strip()


def preprocess_html(raw_html):
    """
    Preprocess HTML string with <ruby> and <rt> tags.
    """
    raw_html = (raw_html.replace("<rt>", ":")
               .replace("</rt>", "")
               .replace("<rb>", "")
               .replace("</rb>", "")
               .replace("<ruby>", "(")
               .replace("</ruby>", ")"))
    raw_html = re.sub('\\n|\\t|\\r', "", raw_html)
    return raw_html


def get_monthly_news_data():
    """
    Each day needs to thread safe, first step is to gather all URL information.
    news_data = [{
        "id"    : integer
        "date"  : string
        "title" : string
    }]
    """
    news_data = []

    request = requests.get(BASE_URI + ENDPOINT["NEWS_LIST"])
    if request.status_code == 200:
        news_dict = json.loads(request.content)[0]
        for news_date in news_dict:
            daily_news_list = news_dict[news_date]
            for news in daily_news_list:
                # Strip out "k" from "k10010999071000"
                news_id = int(news["news_id"][1:])
                news_title = news["title"]
                news_data.append({
                    "id"    : news_id,
                    "date"  : news_date,
                    "title" : news_title
                })
    return news_data
