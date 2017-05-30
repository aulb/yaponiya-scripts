#!/usr/bin/env python                                                                                                                                      
# -*- coding:utf-8 -*-         
import requests
import sqlite3
import csv
from multiprocessing.pool import ThreadPool

from yapohelper import *

connection = sqlite3.connect("yapo.sqlite")
# Each thread gets its own cursor
cursor = connection.cursor()

connection.commit()
connection.close()

"""
First parallelization to check existence
For each one, do a select statement to see if id exist, 
if yes, return []
if no, return [news_id, news_date, news_title]
"""
def check_if_news_exist_if_yes_return_article_id():
    """
    FILTER (news_id, news_date, news_title) => (news_id, news_date, news_title)
    """
    pass



"""
Second parallelization to get statements
For each valid article, 
	- create insert statement, return
	
	pool.map(execute_insert_article, insert_statements)
	MAP (news_id, insert_statements) => (news_id, row_id)
	get reikai urls
	MAP (reikai_urls, row_id) => insert_statements
	pool.map(execute_insert_reikai) => None

	out of order no problemo

	- insert new article to database / create insert statement
	- https://stackoverflow.com/questions/6242756/how-to-retrieve-inserted-id-after-inserting-row-in-sqlite-using-python
	- get article_id in return 
	- reikai below...
	- supply all the readings + words too
"""
def if_news_exist_go_to_url():
    """
    MAP (...)
    """
    pass


def get_reikai_statements(reikai_url, artcile_id):
	pass

# with open("data/url_list.csv", "r") as url_list:
#     urls = csv.reader(url_list, delimiter=",")
#     for row in url_list:
#         news_url, date_string, news_title = row.split(",")
#         news_id = re.match(ID_PATTERN, news_url).groups()[0]
#         print(row)

#         # request.content is the JSON string
#         news_request = requests.get(news_url)
            
#         # Get the word (kanji) - reading pairs from all texts
#         reading_dictionary = {}

#         if news_request.status_code is not 200:
#             continue

#         # Set encoding to utf-8 to
#         news_request.encoding = BASE_ENCODING

#         # Preprocess HTML 
#         news_html = preprocess_html(news_request.text)

#         # Use BeautifulSoup to find the article's main div
#         news_parser = BeautifulSoup(news_html, "html.parser")
#         news_parser = news_parser.find(id=MAIN_DIV_WRAPPER)
        
#         # Get article's raw text
#         get_article_vocab(news_parser.text, reading_dictionary)

#         cursor.execute(INSERT_ARTICLE.format(
#             news_id            = news_id,
#             news_date         = date_string,
#             article_title    = news_title,
#             article_text    = get_article_raw(news_parser.text)
#         ))

#         reikai_url = make_article_url(news_id, "REIKAI")

#         # make a GET request to reikai_url
#         reikai_request = requests.get(reikai_url)
#         if reikai_request.status_code is not 200:
#             continue

#         dictionary_entry = json.loads(reikai_request.content)["reikai"]["entries"]
#         for entry_key in dictionary_entry:
#             current_entry = dictionary_entry[entry_key]
#             for definition_object in current_entry:
#                 word_definition = definition_object["def"] 
#                 word_token = definition_object["hyouki"][0]

#                 word_definition = preprocess_html(word_definition)
#                 word_definition = get_article_raw(word_definition)

#                 get_article_vocab(word_definition, reading_dictionary)

#                 cursor.execute(INSERT_DICTIONARY.format(
#                     article_id     = str(counter),
#                     word         = word_token,
#                     meaning     = word_definition
#                 ))
        
#         for kanji_compound in reading_dictionary:
#             cursor.execute(INSERT_READING.format(
#                 kanji_compound     = kanji_compound,
#                 reading         = reading_dictionary[kanji_compound],
#             ))
        
#         counter += 1
#         connection.commit()

