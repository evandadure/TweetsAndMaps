# -*- coding: utf-8 -*-
import time
import tweepy
import coords
import tokenizer
import database
try:
    import json
except ImportError:
    import simplejson as json



# Variables that contains the user credentials to access Twitter API

ACCESS_TOKEN = '1092775756990742528-f3jdO4dHk6mz74xelnaIR5DanAWPm6'
ACCESS_SECRET = 'ajiXNmSln042ivtOOTh9GYkh0vcJNZwiQAmZMuf6sRCtB'
CONSUMER_KEY = 'nazYTA9BgmjpZSB54whfr4gkF'
CONSUMER_SECRET = 'zOm049TtpKJ4zc36gqD3XV8xl4SYSvQJCz1AygEbDK0BVt5v37'

# ACCESS_TOKEN = '818456674507902977-CweXH1SJkOeyKLAc1EUnZ2JKSHpC83Z'
# ACCESS_SECRET = 'kLla8weNLy1tfEdwEIlUmz9g1tV91sO7VHE5dOhyrYLsL'
# CONSUMER_KEY = 'cZQqU0bI8Du4OAr3vqZFGH17C'
# CONSUMER_SECRET = 'JuFRZeTaWVG48GYALBRDuaJHJr5LQVqBsFyDyyDxaUVYhu0rMz'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


def get_trends(WOEID):
    """
    Gets the biggest Twitter trends of a city.
    ----------
    Parameters :
        - WOEID(str) : the Yahoo's WOEID of the city
    Returns :
        - names(list) : a of the trends (str).
    """
    trends1 = api.trends_place(WOEID) # WOEID of Paris : 615702
    # trends1 is a list with only one element in it, which is a
    # dict which we'll put in data.
    data = trends1[0]
    # grab the trends
    trends = data['trends']
    # grab the name from each trend
    names = [trend['name'] for trend in trends]
    return names


def saveTweets(mydb, mycursor,searched_word="", number_max=10000000,only_located=True,city="Grenoble",country="France",radius="30"):
    """
    Using Twitter API and Tweepy, saves some tweets and their information in your database. Can also save some keywords
    if the tweet has a location.
    ----------
    Parameters :
        - mydb (mysql.connector.connection.MySQLConnection) : the database connection
        - mycursor (mysql.connector.cursor.MySQLCursor) : a cursor of the connection
        - searched_word (str) : specify it if you want all the tweets returned by the API to contain this word
        - number_max (int) : the maximum number of tweets returned before it the research ends
        - only_located (bool) : True if you only want to save located tweets, False if you want all tweets.
            (if False, will set latitude to 0, longitude to 0 and city to 'Unknown'.
        - city (str) : the city where you'd like to search tweet
        - country(str) : the country of the city
        - radius (str) : the radius (in km) of the search zone, around the city
    Returns :
        No return
    """
    #COORDS OF SOME FRENCH CITIES (ex : geocode="45.188529,5.724524,30km")
    #Grenoble : 45.188529,5.724524
    #Paris : 48.853,2.35
    lat,long = coords.getCenterCoords(city,country)
    searchZone = str(lat) + "," + str(long) + "," + radius + "km"
    for status in tweepy.Cursor(api.search, q=searched_word, tweet_mode='extended', geocode=searchZone).items(number_max):
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
                #We're using a try/catch here because sometimes the location can't be found with Geopy's API, and we don't
                #want it to stop our program.
                try:
                    addr_infos = coords.get_address(latitude, longitude)
                    if "county" in addr_infos["address"]:
                        county = addr_infos["address"]["county"]
                        #The list of keywords found in the tweet are also saved in the database, for further analysis.
                        wordList = tokenizer.getKeyWords(tweet_text)
                        database.addKeywords(mydb, mycursor,tweet_id, county, wordList)
                except:
                    pass
            else:
                longitude, latitude = (0,0)
            #only_located is set at True if the user wants to save only the located tweets (False if he wants to save all tweets)
            if not only_located or (only_located and longitude != 0):
                try:
                    print("----------------------------------")
                    print(tweet_text)
                    print("----------------------------------")
                    database.addTweet(mydb, mycursor,tweet_id, tweet_created_at, tweet_text, tweet_user_id, tweet_user_name,
                             tweet_user_screenname, latitude, longitude, searched_word, county)                    
                except:
                    pass
    #Some saved words and keywords were found with some characters that MySQL replaces with question marks, so this function
    #is just "cleaning" the database by deleting the saved words that are only composed of question marks.
    database.deleteQuestionMarksOnly(mydb, mycursor)