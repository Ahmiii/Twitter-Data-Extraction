
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


for i in user_ids:

	file_name="{}.json".format(username+"-Mentios")
	with open(file_name,'w') as f:
		alltweets = []	
		new_tweets = api.user_timeline(user_id = username,count=200)
		alltweets.extend(new_tweets)
			
		oldest = alltweets[-1].id - 1
			
		while len(new_tweets) > 0:
				new_tweets = api.user_timeline(user_id = username,count=200,max_id=oldest)
				alltweets.extend(new_tweets)
				oldest = alltweets[-1].id - 1
		        
		mention = set()
		for i in range(0,len(alltweets)):
		    if alltweets[i].in_reply_to_status_id is None and alltweets[i].retweeted is False:
		        if len(alltweets[i].entities["user_mentions"]) > 0:
		            for j in range(0, len(alltweets[i].entities["user_mentions"])):
		                #mention.add(alltweets[i].entities["user_mentions"][j]["screen_name"])
		                out=user_id,alltweets[i].entities["user_mentions"][j]["screen_name"]
		                f.write(json.dumps(out,default=json_util.default)+','+"\n")