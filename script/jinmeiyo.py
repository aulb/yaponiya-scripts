# -*- coding:utf-8 -*-         
import csv
import sqlite3

sql_filename = "yapo.sqlite"
connection = sqlite3.connect(sql_filename)
cursor = connection.cursor()

CHECK_EXISTENCE = """
SELECT kanji_id
FROM kanji
WHERE kanji = '{kanji}';
"""

INSERT_NEW = """
INSERT INTO kanji
(kanji, is_joyo, is_jinmeiyo)
VALUES
('{kanji}', {is_joyo}, {is_jinmeiyo});
"""

UPDATE_EXISTING = """
UPDATE kanji
SET is_jinmeiyo = 1
WHERE kanji = '{kanji}';
"""

with open("data/tangorin_1000.csv", "rt") as f:
    reader = csv.reader(f)
    for row in reader:
        kanji = row[0].split("\t")[0]
        is_exist = cursor.execute(CHECK_EXISTENCE.format(
            kanji = kanji
        )).fetchone() is not None

        if is_exist:
            print('Exist: ' + kanji)
            cursor.execute(UPDATE_EXISTING.format(
                kanji = kanji
            ))
        else:
            print('Doesnt exist: ' + kanji)
            cursor.execute(INSERT_NEW.format(
                kanji = kanji,
                is_joyo = 0,
                is_jinmeiyo = 1
            ))

connection.commit()
connection.close()
