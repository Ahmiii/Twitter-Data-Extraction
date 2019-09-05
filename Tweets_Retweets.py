
import json
import re
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import urllib
import re
import time
import csv
from bson import json_util

CONSUMER_KEY=""
CONSUMER_SECRET=""
ACCESS_KEY=""
ACCESS_SECRET=""

auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


with open('IDS.csv') as f:
	array = []
	user_ids=[]
	for line in f:
		array.append(line)
	print(array)

for i in array:
 	try:
 		user_ids.append(api.get_user(i).id)
 	except tweepy.error.TweepError as e:
 		continue

file_name="{}.json".format(i+"Tweets_Retweets")
with open(file_name,'w')  as f:
	retweetnetowrk=[]
	print("\n"+"All Tweets and One who retweet Them"+"\n")
	for tweet in api.user_timeline(user_id = username, count=200,tweet_mode='extended'):
		f.write(json.dumps(tweet._json)+','+"\n")
			for reTweet in api.retweets(tweet.id):
				f.write(json.dumps(reTweet._json)+','+"\n")