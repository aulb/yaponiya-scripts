#!/usr/bin/env python                                                                                                                                      
# -*- coding:utf-8 -*-      
"""
Basic scraping:
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

Reikai:
	- Hit the URL
	- Check 200
	- Transform JSON to object, REIKAI, ENTRIES
	- For each entry, get the word:meaning and store 
	- For each meaning, get the reading and store 
"""	
import requests
import re
import json
import collections
import sqlite3
from bs4 import BeautifulSoup

from yapohelper import *

connection = sqlite3.connect("temporary.sqlite")
cursor = connection.cursor()

insert_into_article = """
INSERT INTO nhk_article
	(news_id, news_date, article_title, article_text) 
VALUES 
	('{news_id}', '{news_date}', '{article_title}', '{article_text}');
"""
insert_into_dictionary = """
INSERT INTO nhk_dictionary
	(article_id, word, meaning) 
VALUES 
	('{article_id}', '{word}', '{meaning}');
"""
counter = 1

request = requests.get(BASE_URI + ENDPOINT["NEWS_LIST"])
if request.status_code == 200:
	# request.content is the JSON string
	news_dict = json.loads(request.content)[0]
	for date_string in news_dict:
		current_news_list = news_dict[date_string]
		for news_meta in current_news_list:
			# News URL
			news_id = news_meta["news_id"]
			news_title = news_meta["title"]
			news_web_url = news_meta["news_web_url"]
			news_url = make_article_url(news_id)
			news_request = requests.get(news_url)
			
			# Temporary container
			reading_list = {}
			dictionary_list = {}

			if news_request.status_code is not 200:
				continue

			# Set encoding to utf-8 to
			news_request.encoding = BASE_ENCODING

			# Preprocess HTML 
			news_html = preprocess_html(news_request.text)

			# Use BeautifulSoup to find the article's main div
			news_parser = BeautifulSoup(news_html, "html.parser")
			news_parser = news_parser.find(id=MAIN_DIV_WRAPPER)
			
			# Get article's raw text
			# print(get_article_vocab(news_parser.text))
			print(news_title)
			# print("\n")				
			# print(insert_into_article.format(
			# 	news_id			= news_id,
			# 	news_date 		= date_string,
			# 	article_title	= news_title,
			# 	article_text	= get_article_raw(news_parser.text),
			# ))
			# cursor.execute(insert_into_article.format(
			# 	news_id			= news_id,
			# 	news_date 		= date_string,
			# 	article_title	= news_title,
			# 	article_text	= get_article_raw(news_parser.text)
			# ))

			# if counter is 50:
			# 	counter = 0
			# 	connection.commit()
			# counter += 1
			# break
			reikai_url = make_article_url(news_id, "REIKAI")

			# make a GET request to reikai_url
			reikai_request = requests.get(reikai_url)
			if reikai_request.status_code is not 200:
				continue
			dictionary_entry = json.loads(reikai_request.content)["reikai"]["entries"]
			for entry_key in dictionary_entry:
				current_entry = dictionary_entry[entry_key]
				for definition_object in current_entry:
					word_definition = definition_object["def"] 
					word_token = definition_object["hyouki"][0]

					word_definition = preprocess_html(word_definition)
					word_definition = get_article_raw(word_definition)

					print(insert_into_dictionary.format(
						article_id = str(1),
						word = word_token,
						meaning = word_definition
					))
					cursor.execute(insert_into_dictionary.format(
						article_id = str(1),
						word = word_token,
						meaning = word_definition
					))

connection.commit()
connection.close()

