# Installation guide:
Make sure to get the right python3 wrapper and download MeCab and its python wrapper.

## Resources:
- http://www.statsbeginner.net/entry/2016/02/05/020027 
- http://www.robfahey.co.uk/blog/tidying-japanese-sns-data-machine-learning/
- http://takegue.hatenablog.com/entry/2015/01/25/045341
- http://qiita.com/Salinger/items/529a77f2ceeb39998665
- http://www.atilika.org/

## Python Dependencies:
- requests
- tweepy
- oauth2
- beautifulsoup4
- pymongo
- praw
- scrapy (not needed)

捗る→

# NHKArticle
id,news_id,title,article,news_url

# NHKEasyDictionary
id,news_id,word,meaning

# NHKMostCommonReading
id,word,reading

# NHKEasyCounter
id,kanji,counter

捗る→

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
    * title             : Japanese title without reading
    * title_with_ruby     : Japanese title with reading
    * news_id             : Where the article is located
    * news_web_url        : Where the non-easy version is located

Reikai:
    - Hit the URL
    - Check 200
    - Transform JSON to object, REIKAI, ENTRIES
    - For each entry, get the word:meaning and store 
    - For each meaning, get the reading and store 
""" 