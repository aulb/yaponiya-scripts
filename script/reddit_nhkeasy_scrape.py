# -*- coding:utf-8 -*-
import praw

url_list = open("url_list", "w")

reddit = praw.Reddit(
	client_id		= "",
	client_secret	= "",
	password		= "",
	user_agent		= "",
	username		= ""
)

nhksub = reddit.subreddit('NHKEasyNews').submissions(1292112000, 1495432961)
urlrow = "{url},{title}\n"

for sub in nhksub:
	print(sub.title)
	try:
		url = sub.selftext.split()[0]
		if "http" not in url:
			continue
		url_list.write(urlrow.format(url=url, title=sub.title))
	except:
		continue
