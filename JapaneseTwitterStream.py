# -*- coding:utf-8 -*-
import json
import re 

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from JapaneseScriptMatcher import *

consumer_key = 'fTU9ICQB34Z3ELH9cZswqCeel'
consumer_secret = 'ZW8jwwfVYSVvdihVCzgIVleHu05x7NwGGDidPgPBzeWi1HVkoT'
access_token = '81681631-kvpRdgoSIOkJLLBSFG8dInFkkwuM5oBT2mwiZfRhN'
access_token_secret = 'YqcSS8tFQpLSvtmjPkFaEloAqO9c6SxcWkQn5bRZTPZVz'

class StdOutListener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        clip_all_but = "".join(list(filter(is_kanji, data["text"])))
        print(clip_all_but)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(locations=[129.484177, 30.923179, 145.985641, 45.799878])
