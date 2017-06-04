#!/usr/bin/env python                                                                                                                                      
# -*- coding:utf-8 -*-         
import sqlite3
import csv
import time
from multiprocessing.pool import ThreadPool

from yapohelper import *

SQL_FILENAME = "yapo.sqlite"

def create_connection(sql_filename):
    connection = sqlite3.connect(sql_filename)
    cursor = connection.cursor()
    return connection, cursor

def close_connection(connection, commit=False):
    if commit:
        connection.commit()
    connection.close()

def pool_filter(pool, func, candidates):
    return [c for c, keep in zip(candidates, pool.map(func, candidates)) if keep]

def check_existence(data):
    connection, cursor = create_connection(SQL_FILENAME)
    id = cursor.execute(SELECT_ARTICLE.format(news_id=data["id"])).fetchone()
    close_connection(connection)
    if id is None:
        return True
    return False

def store_to_db(data):
    # TODO: Needs refactoring 
    # TODO: Async cursor
    reading_dictionary = {}

    news_id = data["id"]
    news_date = data["date"]
    news_title = data["title"]
    print(news_title)
    # Make news_url
    news_url = make_article_url("k" + str(news_id))

    news_request = requests.get(news_url)
    # retries 5 times with sleep
    if news_request.status_code is not 200:
        return

    connection, cursor = create_connection(SQL_FILENAME)

    # Set encoding to utf-8 to
    news_request.encoding = BASE_ENCODING

    # Preprocess HTML 
    news_html = preprocess_html(news_request.text)

    # Use BeautifulSoup to find the article's main div
    news_parser = BeautifulSoup(news_html, "html.parser")
    news_parser = news_parser.find(id=MAIN_DIV_WRAPPER)
    
    # Get article's raw text
    get_article_vocab(news_parser.text, reading_dictionary)

    cursor.execute(INSERT_ARTICLE.format(
        news_id       = news_id,
        news_date     = news_date,
        article_title = news_title,
        article_text  = get_article_raw(news_parser.text)
    ))

    article_id = cursor.lastrowid
    reikai_url = make_article_url("k" + str(news_id), "REIKAI")

    # make a GET request to reikai_url
    reikai_request = requests.get(reikai_url)
    if reikai_request.status_code is 200:
        dictionary_entry = json.loads(reikai_request.content)["reikai"]["entries"]
        for entry_key in dictionary_entry:
            current_entry = dictionary_entry[entry_key]
            for definition_object in current_entry:
                word_definition = definition_object["def"] 
                word_token = definition_object["hyouki"][0]

                word_definition = preprocess_html(word_definition)
                word_definition = get_article_raw(word_definition)

                get_article_vocab(word_definition, reading_dictionary)

                cursor.execute(INSERT_DICTIONARY.format(
                    article_id = str(article_id),
                    word       = word_token,
                    meaning    = word_definition
                ))

    for kanji_compound in reading_dictionary:
        cursor.execute(INSERT_READING.format(
            kanji_compound = kanji_compound,
            reading        = reading_dictionary[kanji_compound],
        ))

    close_connection(connection, commit=True)
    return

monthly_data = get_monthly_news_data()
# Check which data does not exist
pool = ThreadPool(15)
new_data = pool_filter(pool, check_existence, monthly_data)

# Store to db sequentially
for data in new_data:
    store_to_db(data)

