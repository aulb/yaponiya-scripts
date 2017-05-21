#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-      
import requests
import re
import json
from bs4 import BeautifulSoup

BASE_URI = "http://www3.nhk.or.jp/news/"
ENDPOINT = {
	"TOP_NEWS"		: "easy/top-list.json",
	"NEWS_LIST"		: "easy/news-list.json",
	"KOYOMI"		: "json/koyomi.json",
	"REIKAI"		: "easy/{news_id}/{news_id}.out.dic",
	"NEWS_ARTICLE"	: "easy/{news_id}/{news_id}.html" 
}
MAIN_DIV_WRAPPER = "newsarticle"
PATTERN = r'\((\w+):(\w+)\)'

TEST_URI = "http://www3.nhk.or.jp/news/easy/k10014977351000/k10014977351000.html"

# request = requests.get(TEST_URI)
# request.encoding = "utf-8"

# html = request.text.replace("<rt>", ":").replace("</rt>", "").replace("<ruby>", "(").replace("</ruby>", ")")
# html = re.sub('\\n|\\t|\\r', "", html)

# # Strip all anchors + spans

# soup = BeautifulSoup(html, "html.parser")
# soup = soup.find(id="newsarticle")

"""

"""
def main():
	news_url = make_article_url(news_article["news_id"])
	request = requests.get(news_url)

	# request = requests.get(TEST_URI)
	# request.encoding = "utf-8"

	# html = request.text.replace("<rt>", ":").replace("</rt>", "").replace("<ruby>", "(").replace("</ruby>", ")")
	# html = re.sub('\\n|\\t|\\r', "", html)
	pass


"""
Return url.
"""
def make_article_url(news_id):
	return BASE_URI + ENDPOINT["NEWS_ARTICLE"].format(news_id=news_id)

"""
Get raw.
"""
def scrape_article(news_url):

	return

"""
Parse per article. 
Make word + reading vocabulary list.
"""
def get_article_vocab(preprocessed_string):
	matches = re.findall(PATTERN, preprocessed_string)
	vocab_dict = {}
	for word, reading in matches:
		if word not in vocab_dict:
			vocab_dict[word] = reading
	return vocab_dict

"""
Return article's raw text without kanji's reading. 
"""
def get_article_raw(preprocessed_string):
	return re.sub(PATTERN, r'\1', preprocessed_string)


if __name__ == '__main__':
	"""
	- GET request to NEWS_LIST, this gets you a monthly list as a JSON string.
	- Processed the JSON string into a python dictionary.
	- For each dictionary key which is the date_string, get the news list for each day.
	- For each daily news, get the news_id, title, title with ruby
	- For each news article:
		- GET request to the article's location
		- Parse the article, get the following:
			- Article's raw text
			- Kanji list with reading
		* title 			: Japanese title without reading
		* title_with_ruby 	: Japanese title with reading
		* news_id 			: Where the article is located
		* news_web_url		: Where the non-easy version is located

	"""	
	request = requests.get(BASE_URI + ENDPOINT["NEWS_LIST"])
	if request.status_code == 200:
		# request.content is the JSON string
		news_dict = json.loads(request.content)[0]
		for date_string in news_dict:
			current_news_list = news_dict[date_string]
			for news_article in current_news_list:
				print(news_article["title_with_ruby"], news_article["news_id"])

	