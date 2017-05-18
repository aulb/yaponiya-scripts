#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-      

import scrapy
import requests
import time
import re
from bs4 import BeautifulSoup


BASE_URI = "http://www3.nhk.or.jp/news/easy"

ENDPOINT_TOP_LIST = "top-list.json" # ?_=1494735367139
ENDPOINT_NEWS_LIST = "news-list.json"
ENDPOINT_KOYOMI = "koyomi.json"

MAIN_DIV_WRAPPER = "newsarticle"

TEST_URI = "http://www3.nhk.or.jp/news/easy/k10014977351000/k10014977351000.html"

request = requests.get(TEST_URI)
request.encoding = "utf-8"

html = request.text.replace("<rt>", ":").replace("</rt>", "")
html = re.sub('\\n|\\t|\\r', "", html)

# .replace("\n", "")
# .replace("\t", "")
# .replace("\r", "").

# Strip all anchors + spans

soup = BeautifulSoup(html, "html.parser")
soup = soup.find(id="newsarticle")

"""
Return url.
"""
def make_url(id):
	return 

"""
Get raw.
"""
def scrape_article(url):
	return


"""
Parse per article. Return text article.
# span:#under
# a:.dicWin, ignored with BeautifulSoup's API. Call .ruby on .contents.

Make word + reading vocabulary list.
"""
def get_article(paragraphs):
	for paragraph in paragraphs.contents:
		# First pass to get rid of anchors/spans
		pass
	pass


def parse_paragraph(paragraph):
	return
