# -*- coding: utf-8 -*-

# TO DO :
# - méthode qui supprime les doublons dans la base de données
# - possibilité d'aller chercher des anciens tweets (pour ne pas reprendre les mêmes)




# Import the necessary package to process data in JSON format
import mysql.connector
import tweepy
import coords
from datetime import datetime, timedelta
try:
    import json
except ImportError:
    import simplejson as json












# Variables that contains the user credentials to access Twitter API

# ACCESS_TOKEN = '1092775756990742528-f3jdO4dHk6mz74xelnaIR5DanAWPm6'
# ACCESS_SECRET = 'ajiXNmSln042ivtOOTh9GYkh0vcJNZwiQAmZMuf6sRCtB'
# CONSUMER_KEY = 'nazYTA9BgmjpZSB54whfr4gkF'
# CONSUMER_SECRET = 'zOm049TtpKJ4zc36gqD3XV8xl4SYSvQJCz1AygEbDK0BVt5v37'

ACCESS_TOKEN = '818456674507902977-CweXH1SJkOeyKLAc1EUnZ2JKSHpC83Z'
ACCESS_SECRET = 'kLla8weNLy1tfEdwEIlUmz9g1tV91sO7VHE5dOhyrYLsL'
CONSUMER_KEY = '5HmCS4zWFTa47hJHa3KKOknDE'
CONSUMER_SECRET = 'pMKmFuHeY5Xzo4LOcGQIxCSo18GALolGfn927p5cKjpWeRMxWI'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)


# CONNECTION TO THE DATABASE
# =============================================================================
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="isoc_tp_twitter"
)
mycursor = mydb.cursor()
# =============================================================================


def setDateTime(dateTweet):
    """
    Fonction qui crée un datetime à partir d'une string de date (exemple "21/08/18"), et d'une string d'heure (exemple "13:37")
    Parametres :
        - date : String de la date
        - heure : String de l'heure
    Retourne :
        d : la date (et son heure) dans le type datetime
    """
    monthsDic  = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    dateToString = dateTweet[8:10]+"/"+monthsDic[dateTweet[4:7]]+"/"+dateTweet[-2:]
    d = datetime.strptime(dateToString,"%d/%m/%y")
    h = dateTweet[dateTweet.find(':')-2:dateTweet.find(':')]
    m = dateTweet[dateTweet.find(':')+1:dateTweet.find(':')+3]
    d = d.replace(hour=int(h),minute=int(m))
    d = d + timedelta(hours=1)
    return d

# METHODES DE TRAITEMENT DES LONGITUDES/LATITUDES AFFICHEES DANS UN TWEET
# Ces méthodes font la moyennes des valeurs du "polygone" de la localisation d'un tweet
# =============================================================================
def getLongAndLat(listeCouplesCoord):
    listeLongitude = []
    listeLatitude = []
    for couple in listeCouplesCoord:
        listeLongitude.append(couple[0])
        listeLatitude.append(couple[1])
    return (listeLongitude,listeLatitude)

def moyList(list):
    return (sum(list)/len(list))


def centrePolygone(list_Longitude, list_Latitude):
    return [moyList(list_Longitude), moyList(list_Latitude)]


def saveTweets(keyword, number_max,only_located):
    #COORDS OF SOME FRENCH CITIES (ex : geocode="45.188529,5.724524,30km")
    #Grenoble : 45.188529,5.724524
    #Paris : 48.853,2.35
    for status in tweepy.Cursor(api.search, q=keyword, geocode="45.188529,5.724524,30km").items(number_max):
        county="unknown"
        tweet = status._json
        tweet_id = tweet['id'] #the id of the tweet/retweet
        tweet_created_at = setDateTime(tweet['created_at']) # when the tweet posted
        tweet_text = tweet['text'] # content of the tweet
        tweet_user_id = tweet['user']['id'] # id of the user who posted the tweet
        tweet_user_name = tweet['user']['name'] # name of the user, e.g. "Wei Xu"
        tweet_user_screenname = tweet['user']['screen_name'] # name of the user account, e.g. "cocoweixu"
        #Only the real tweets are stored, not the retweets.
        if tweet_text[:2]!="RT":
            #IF THE USER SPECIFIED HIS LOCATION IN HIS TWEET, THIS LOCATION IS SAVED IN THE DATABASE AND THE TWEET IS DISPLAYED ON A MAP
            if tweet['place'] is not None and tweet['place']['bounding_box'] is not None and tweet['place']['bounding_box']['coordinates'] is not None:
                longitude, latitude = getLongAndLat(tweet['place']['bounding_box']['coordinates'][0])
                longitude, latitude = centrePolygone(longitude, latitude)
                try:
                    addr_infos = coords.get_address(latitude, longitude)
                    if "county" in addr_infos["address"]:
                        county = addr_infos["address"]["county"]
                except:
                    pass
            else:
                longitude, latitude = (0,0)
            #only_located is set at True if the user wants to save only the located tweets (False if he wants to save all tweets)
            if not only_located or (only_located and longitude != 0):
                sql = "INSERT INTO tweet (created_at, text, user_ID, user_name, screen_name, latitude, longitude, keyword,\
                                            nearest_city, id_tweet) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (tweet_created_at, tweet_text, tweet_user_id, tweet_user_name, tweet_user_screenname, latitude, longitude, keyword, county, tweet_id)
                mycursor.execute(sql, val)
                mydb.commit()

def displayAllTweets(city="",keyword=""):
    mycursor.execute("SELECT * FROM tweet WHERE nearest_city LIKE '%"+city+"%' AND keyword LIKE '%"+keyword+"%'")
    myresult = mycursor.fetchall()
    map = coords.create_map()
    for line in myresult:
        if line[6] != "0":
            addr_infos = coords.get_address(line[6], line[7])
            coords.add_marker(map, float(line[6]), float(line[7]), line[4], line[5], line[2],
                              str(line[1]), addr_infos["display_name"])
    map.save('map.html')




#displayAllTweets(keyword="salut")
saveTweets("", 10000,True)


# =============================================================================

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

# code pour écrire dans un fichier texte le résultat d'une requete
# =============================================================================
# with open('twitter_stream_200tweets.json','w') as outfile:
# #REQUETE
# #-----------------------------------
#     for status in tweepy.Cursor(api.home_timeline).items(50):
#         print(status._json)
# #-----------------------------------
#         res = status._json
#         json.dump(res, outfile)
#         outfile.write("\n")

# We use the file saved from last step as example

# tweets_filename = 'twitter_stream_200tweets.json'
# tweets_file = open(tweets_filename, "r")

# for line in tweets_file:
#     try:
#         # Read in one line of the file, convert it into a json object
#         tweet = json.loads(line.strip())
#         if 'text' in tweet: # only messages contains 'text' field is a tweet
#             print(tweet['id']) # This is the tweet's id
#             print(tweet['created_at']) # when the tweet posted
#             print(tweet['text']) # content of the tweet
#
#             print(tweet['user']['id']) # id of the user who posted the tweet
#             print(tweet['user']['name']) # name of the user, e.g. "Wei Xu"
#             print(tweet['user']['screen_name']) # name of the user account, e.g. "cocoweixu"
#
#             hashtags = []
#             for hashtag in tweet['entities']['hashtags']:
#                 hashtags.append(hashtag['text'])
#             print(hashtags)
#
#     except:
#         # read in a line is not in JSON format (sometimes error occured)
#         continue
# =============================================================================

# code pour s'abonner à un autre user
# =============================================================================
# api.create_friendship('@ThomasB72832506')
# =============================================================================




