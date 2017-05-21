#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-      
import requests
import re
import json
import collections
from bs4 import BeautifulSoup

BASE_URI = "http://www3.nhk.or.jp/news/"
BASE_ENCODING = 'utf-8'
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

"""NHK Easy News extractor.

Extracts all needed information from an NHK Easy News article.
"""
NHKEasyNews = collections.namedtuple('NHKEasyNews', 'title vocab_list news_with_title')

"""

"""
def main():
	pass


"""
Return url.
"""
def make_article_url(news_id, endpoint="NEWS_ARTICLE"):
	return BASE_URI + ENDPOINT[endpoint].format(news_id=news_id)


"""
Get raw.
"""
def scrape_article(news_url):
	return


"""
Parse per article. 
Make word + reading vocabulary list.
"""
def get_article_vocab(preprocessed_string, vocab_dict={}):
	matches = re.findall(PATTERN, preprocessed_string)
	vocab_dict = {}
	for word, reading in matches:
		vocab_dict[word] = reading
	return vocab_dict


"""
Return article's raw text without kanji's reading. 
"""
def get_article_raw(preprocessed_string):
	return re.sub(PATTERN, r'\1', preprocessed_string)


"""
Preprocess HTML string with <ruby> and <rt> tags.
"""
def preprocess_html(raw_html):
	raw_html = (raw_html.replace("<rt>", ":") 
					   	.replace("</rt>", "") 
					   	.replace("<rb>", "")
					   	.replace("</rb>", "")
					   	.replace("<ruby>", "(") 
					   	.replace("</ruby>", ")"))
	raw_html = re.sub('\\n|\\t|\\r', "", raw_html)
	return raw_html


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
			- Dictionary
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
			for news_meta in current_news_list:
				# News URL
				news_url = make_article_url(news_meta["news_id"])
				news_request = requests.get(news_url)

				if request.status_code is not 200:
					continue

				# Set encoding to utf-8 to
				news_request.encoding = BASE_ENCODING

				# Preprocess HTML 
				news_html = preprocess_html(news_request.text)

				# Use BeautifulSoup to find the article's main div
				news_parser = BeautifulSoup(news_html, "html.parser")
				news_parser = news_parser.find(id=MAIN_DIV_WRAPPER)
				
				# Get article's raw text
				print(get_article_vocab(news_parser.text))
				break;
			break;
				# Get kanji list with reading
				# print(news_meta["title_with_ruby"], news_meta["news_id"])	
	# ['reikai']['entries'][0]



	request = requests.get(make_article_url(news_meta["news_id"], "REIKAI"))
	current_dictionary = json.loads(request.content)["reikai"]["entries"]
	current_dictionary = current_dictionary['0000'][0]['def']


