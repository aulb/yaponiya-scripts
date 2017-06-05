# -*- coding:utf-8 -*-      
import sqlite3
import os

connection = sqlite3.connect("yapo.sqlite")
cursor = connection.cursor()

NHKEasyArticle = """
CREATE TABLE nhk_article 
    (article_id    INTEGER PRIMARY KEY AUTOINCREMENT,
     news_id       INTEGER NOT NULL,
     news_date     DATE NOT NULL,
     article_title VARCHAR(64) NOT NULL,
     article_text  TEXT NOT NULL)
"""

NHKEasyDictionary = """
CREATE TABLE nhk_dictionary 
    (dictionary_id INTEGER PRIMARY KEY AUTOINCREMENT,
     article_id    INTEGER NOT NULL,
     word          VARCHAR(32) NOT NULL,
     meaning       TEXT NOT NULL,
     FOREIGN KEY(article_id) REFERENCES nhk_article(article_id))
"""

NHKMostCommonReading = """
CREATE TABLE nhk_common_reading
    (reading_id     INTEGER PRIMARY KEY AUTOINCREMENT,
     kanji_compound VARCHAR(32) NOT NULL,
     reading        VARCHAR(32) NOT NULL)
"""

KanjiList = """
CREATE TABLE kanji
    (kanji_id        INTEGER PRIMARY KEY AUTOINCREMENT,
     character       VARCHAR(16) NOT NULL,
     is_joyo         INTEGER NOT NULL,
     is_jinmeiyo     INTEGER,
     onyomi          VARCHAR(32),
     kunyomi         VARCHAR(64),
     jlpt            INTEGER,
     grade           INTEGER,
     meaning         TEXT)
"""

NHKEasyCounter = """
CREATE TABLE nhk_kanji
    (counter_id INTEGER PRIMARY KEY AUTOINCREMENT,
     kanji_id   INTEGER,
     counter    INTEGER NOT NULL,
     week       INTEGER NOT NULL,
     FOREIGN KEY(kanji_id) REFERENCES kanji(kanji_id))
"""

cursor.execute(NHKEasyArticle)
cursor.execute(NHKEasyDictionary)
cursor.execute(NHKMostCommonReading)
cursor.execute(KanjiList)
cursor.execute(NHKEasyCounter)

# Close everything
connection.commit()
connection.close()
