
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
print(user_ids)

for i in user_ids:

	file_name="{}.json".format(username+"Listed")
	with open(file_name,'w')  as f:
		print("\n"+"People Whom listed me"+"\n")

		uss = api.lists_memberships(username)

		#print("People Who Has listed me")
		us = []
		for i in range(0,len(uss)):
		    us.append(uss[i].user.screen_name)
		    out=user_id,uss[i].user.screen_name
		    f.write(json.dumps(out,default=json_util.default)+','+"\n")