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
	
	file_name="{}.json".format(username+"Favouries")
	with open(file_name,'w')  as f:
		print("\n"+"People Whom I favourite"+"\n")
		allfav = []	
		uss = api.favorites(user_id = username,count=200)
		allfav.extend(uss)
		oldest = allfav[-1].id - 1

		while len(uss) > 0:
		    print ("getting favourites before %s" % (oldest))
				
		    uss = api.favorites(user_id = username,count=200,max_id=oldest)
				
		    allfav.extend(uss)

		    oldest = allfav[-1].id - 1


		fav = set()
		for i in range(0, len(allfav)):
		    #fav.add(allfav[i].user.screen_name)
		    out=allfav[i].id,allfav[i].user.id
		    f.write(json.dumps(out,default=json_util.default)+','+"\n")