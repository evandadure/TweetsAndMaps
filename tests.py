
import tweepy
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


for status in tweepy.Cursor(api.search,q="droite", geocode="45.188529,5.724524,30km", tweet_mode='extended').items(10):
    tweet = status._json
    tweet_id = tweet['full_text'] #the id of the tweet/retweet
    print(tweet_id)