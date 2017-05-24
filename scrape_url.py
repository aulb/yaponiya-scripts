# -*- coding:utf-8 -*-      
import requests
import csv

ID_PATTERN 	= r'k[0-9]{14}'
URL_LIST 	= "data/url_list.csv"

with open(URL_LIST, "r") as url_list:
	urls = csv.reader(url_list, delimiter=",")
	for row in url_list:
		url = row.split(",")[0]
		request = requests.get(url)
		if request.status is not 200:
			continue
		
