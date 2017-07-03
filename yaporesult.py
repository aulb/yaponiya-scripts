# -*- coding:utf-8 -*-
import csv
import json
import datetime
import sqlite3

"""
Initial kanji counting.
"""
SQL_FILENAME = "yapo.sqlite"
OUT_FILENAME = "result.json"

SELECT_ARTICLE_BETWEEN = """
SELECT article_title, article_text
FROM nhk_article
WHERE news_date BETWEEN '{start_date}' AND '{end_date}'
"""

def is_kanji(character):
    return 0x4e00 <= ord(character) <= 0x9faf

def count_kanji_article(article, counter={}):
    article_title, article_text = article

    # Process both at once
    for character in article_title + article_text:
        if is_kanji(character):
            counter[character] = counter.get(character, 0) + 1

    return counter

if __name__ == '__main__':
    connection = sqlite3.connect(SQL_FILENAME)
    cursor = connection.cursor()
    start_date = datetime.date(2015, 1, 1)
    end_date = datetime.datetime.today()

    articles = cursor.execute(SELECT_ARTICLE_BETWEEN.format(
        start_date = str(start_date),
        end_date = str(end_date)
    )).fetchall()

    kanji_counter = {}
    for article in articles:
        kanji_counter = count_kanji_article(article, kanji_counter)

    with open(OUT_FILENAME, "w") as outfile:
        outfile.write(json.dumps(kanji_counter, ensure_ascii=False))

    connection.commit()
    connection.close()
