# -*- coding: utf-8 -*-


import tweepy
import coords
import tokenizer
import database
try:
    import json
except ImportError:
    import simplejson as json



# Variables that contains the user credentials to access Twitter API

#ACCESS_TOKEN = '1092775756990742528-f3jdO4dHk6mz74xelnaIR5DanAWPm6'
#ACCESS_SECRET = 'ajiXNmSln042ivtOOTh9GYkh0vcJNZwiQAmZMuf6sRCtB'
#CONSUMER_KEY = 'nazYTA9BgmjpZSB54whfr4gkF'
#CONSUMER_SECRET = 'zOm049TtpKJ4zc36gqD3XV8xl4SYSvQJCz1AygEbDK0BVt5v37'

ACCESS_TOKEN = '818456674507902977-CweXH1SJkOeyKLAc1EUnZ2JKSHpC83Z'
ACCESS_SECRET = 'kLla8weNLy1tfEdwEIlUmz9g1tV91sO7VHE5dOhyrYLsL'
CONSUMER_KEY = 'cZQqU0bI8Du4OAr3vqZFGH17C'
CONSUMER_SECRET = 'JuFRZeTaWVG48GYALBRDuaJHJr5LQVqBsFyDyyDxaUVYhu0rMz'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


def get_trends(WOEID):
    trends1 = api.trends_place(WOEID) # WOEID of Paris : 615702
    # trends1 is a list with only one element in it, which is a
    # dict which we'll put in data.
    data = trends1[0]
    # grab the trends
    trends = data['trends']
    # grab the name from each trend
    names = [trend['name'] for trend in trends]
    return names


def saveTweets(mydb, mycursor,searched_word="", number_max=10000000,only_located=True):
    #COORDS OF SOME FRENCH CITIES (ex : geocode="45.188529,5.724524,30km")
    #Grenoble : 45.188529,5.724524
    #Paris : 48.853,2.35
    for status in tweepy.Cursor(api.search, q=searched_word, tweet_mode='extended',geocode="45.188529,5.724524,30km").items(number_max):
        county="unknown"
        tweet = status._json
        tweet_id = tweet['id'] #the id of the tweet/retweet
        tweet_created_at = database.setDateTime(tweet['created_at']) # when the tweet posted
        tweet_text = tweet['full_text'] # content of the tweet
        tweet_user_id = tweet['user']['id'] # id of the user who posted the tweet
        tweet_user_name = tweet['user']['name'] # name of the user, e.g. "Wei Xu"
        tweet_user_screenname = tweet['user']['screen_name'] # name of the user account, e.g. "cocoweixu"
        #Only the real tweets are stored, not the retweets.
        if tweet_text[:2]!="RT":
            #IF THE USER SPECIFIED HIS LOCATION IN HIS TWEET, THIS LOCATION IS SAVED IN THE DATABASE AND THE TWEET IS DISPLAYED ON A MAP
            if tweet['place'] is not None and tweet['place']['bounding_box'] is not None and tweet['place']['bounding_box']['coordinates'] is not None:
                longitude, latitude = coords.getLongAndLat(tweet['place']['bounding_box']['coordinates'][0])
                longitude, latitude = coords.centrePolygone(longitude, latitude)
                try:
                    addr_infos = coords.get_address(latitude, longitude)
                    if "county" in addr_infos["address"]:
                        county = addr_infos["address"]["county"]
                        wordList = tokenizer.getKeyWords(tweet_text)
                        database.addKeywords(mydb, mycursor,tweet_id, county, wordList)
                except:
                    pass
            else:
                longitude, latitude = (0,0)
            #only_located is set at True if the user wants to save only the located tweets (False if he wants to save all tweets)
            if not only_located or (only_located and longitude != 0):
                try:
                    print(tweet_text)
                    database.addTweet(mydb, mycursor,tweet_id, tweet_created_at, tweet_text, tweet_user_id, tweet_user_name,
                             tweet_user_screenname, latitude, longitude, searched_word, county)                    
                except:
                    pass
    #Certains mots et mots-clés enregistrés, notamment composés de caractères que MySQL ne sait pas gérer et remplace donc par des "?",
    #sont supprimés grâce à la fonction suivante :
    database.deleteQuestionMarksOnly(mydb, mycursor)





















# REQUETES SELECT
# =============================================================================
# mycursor = mydb.cursor()
# mycursor.execute("SELECT * FROM tweet")
# myresult = mycursor.fetchall()
# for line in myresult:
#     print(line)
# print(type(line))
# =============================================================================


# Recherche de mes derniers tweets
# =============================================================================
# tweets=api.user_timeline()
# for tweet in tweets:
#     print(tweet.text)
# =============================================================================

