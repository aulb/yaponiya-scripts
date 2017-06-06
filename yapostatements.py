# -*- coding:utf-8 -*-
# Temporary database statements
INSERT_ARTICLE = """
INSERT INTO nhk_article
    (news_id, news_date, article_title, article_text) 
VALUES 
    ('{news_id}', '{news_date}', '{article_title}', '{article_text}');
"""
INSERT_DICTIONARY = """
INSERT INTO nhk_dictionary
    (article_id, word, meaning) 
VALUES 
    ('{article_id}', '{word}', '{meaning}');
"""

INSERT_READING = """
INSERT INTO nhk_common_reading
    (kanji_compound, reading)
VALUES
    ('{kanji_compound}', '{reading}');
"""

SELECT_ARTICLE = """
SELECT article_id
FROM nhk_article
WHERE news_id = '{news_id}'
"""

RESULT = """
SELECT *
FROM
(SELECT SUM(nk.counter) c, k.character, k.kanji_id, is_joyo
FROM nhk_kanji nk JOIN kanji k ON k.kanji_id = nk.kanji_id
GROUP BY k.kanji_id) t
ORDER BY t.c DESC
"""

"""
# Coordinates for most of Japan
japan = "129.484177, 30.923179, 145.985641, 45.799878"
"""