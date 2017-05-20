import collections
import requests
import time
import re
from bs4 import BeautifulSoup         

PATTERN = r'\((\w+):(\w+)\)'

"""
Parse per article. 
Make word + reading vocabulary list.
"""
def get_article_vocab(preprocessed_string):
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


"""NHK Easy News extractor.

Extracts all needed information from an NHK Easy News article.
"""
NHKEasyNews = collections.namedtuple('NHKEasyNews', 'title title1 title2')