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

	file_name="{}.json".format(username+"Favourited")
	with open(file_name,'w')  as f:
		def get_user_ids_of_post_likes(post_id):
		    try:
		        json_data = urllib.request.urlopen('https://twitter.com/i/activity/favorited_popup?id=' + str(post_id)).read()
		        json_data = json_data.decode('utf-8')
		        found_ids = re.findall(r'data-user-id=\\"+\d+', json_data)
		        unique_ids = list(set([re.findall(r'\d+', match)[0] for match in found_ids]))
		        return unique_ids

		    except urllib.request.HTTPError:
		        pass

		alltweets = []	
		new_tweets = api.user_timeline(user_id = username,count=200)
		alltweets.extend(new_tweets)
			
		oldest = alltweets[-1].id - 1
			
		while len(new_tweets) > 0:
				new_tweets = api.user_timeline(user_id = username,count=200,max_id=oldest)
				alltweets.extend(new_tweets)
				oldest = alltweets[-1].id - 1

		ids = []
		for i in range(0,len(alltweets)):
		    if(alltweets[i].favorite_count > 0):
		        ids.extend(get_user_ids_of_post_likes(alltweets[i].id))
		        out=alltweets[i].id,get_user_ids_of_post_likes(alltweets[i].id)
		        f.write(json.dumps(out,default=json_util.default)+','+"\n")

		uniqueids = set(ids)

		for i in uniqueids:
		    user = api.get_user(i)
		    out=user_id,user.screen_name
		    f.write(json.dumps(out,default=json_util.default)+','+"\n")

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
		    fav.add(allfav[i].user.screen_name)
		    out=user_id,allfav[i].user.screen_name
		    f.write(json.dumps(out,default=json_util.default)+','+"\n")