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

############################################### All tweets and the one who retweet them ##############################################
file_name="{}.json".format(i+"Tweets_Retweets")
with open(file_name,'w')  as f:
	retweetnetowrk=[]
	print("\n"+"All Tweets and One who retweet Them"+"\n")
	for tweet in api.user_timeline(user_id = username, count=200,tweet_mode='extended'):
		f.write(json.dumps(tweet._json)+','+"\n")
			for reTweet in api.retweets(tweet.id):
				f.write(json.dumps(reTweet._json)+','+"\n")

################################################################################################################################
	
	file_name="{}.json".format(username+"-Friends")
	with open(file_name,'w') as f:
		print("\n"+"User Follwoings"+"\n")
		for user in tweepy.Cursor(api.friends, user_id=username).items():
			out=user_id,user.screen_name
			f.write(json.dumps(out,default=json_util.default)+','+"\n")
	
	file_name="{}.json".format(username+"-Followers")
	with open(file_name,'w') as f:		
		print("\n"+"User Follwers"+"\n")
		for user in tweepy.Cursor(api.followers, user_id=username).items():
			out=user_id,user.screen_name
			f.write(json.dumps(out,default=json_util.default)+','+"\n")

####################################################################################################################
	
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

#######################################################################################################################################

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

# #################################################################################################################33
	
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

# ####################################################################################################################################
	
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

####################################################################################################################################
	
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
#####################################################################################################################################3