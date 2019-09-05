
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

for i in array:
 	try:
 		user_ids.append(api.get_user(i).id)
 	except tweepy.error.TweepError as e:
 		continue

for i in user_ids:

	file_name="{}.json".format(username+"List")
	with open(file_name,'w')  as f:
		lists=[]
		uss = api.lists_all(username)
		print("People Whom I listed")
		for i in range(0,len(uss)):
		    if(uss[i].user.screen_name == username):
		    	lists.append(uss[i].name)
		print(lists)
		try:
			for i in lists:
				the_list = api.list_members(username, i)
				print(i)
				for user in the_list:
					out=user_id,user.screen_name
					f.write(json.dumps(out,default=json_util.default)+','+"\n")
		except tweepy.error.TweepError as e:
			continue