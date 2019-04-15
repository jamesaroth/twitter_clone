# from ..controllers.util import hash_pass
import time
from datetime import datetime

from .orm import ORM
from .account import Account

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

class Tweet(ORM):
    fields = ['account_pk', 'username', 'tweet_text', 'time', 'retweet_count', 'likes']
    table = 'tweets'

    def __init__(self):
        self.pk = None
        self.account_pk = None
        self.tweet_text = None
        self.time = None
        self.username = None
        self.retweet_count = 0
        self.likes = 0

    def get_username(self):
        user = Account.from_pk(self.account_pk)
        self.username = user.username
        return user.username

def get_tweets_for_user(account_pk):
    """ return a list of each Tweet object for this user """
    where = "WHERE account_pk = ?"
    values = (account_pk, )
    orders = "ORDER BY time DESC"
    return Tweet.select_many(where, orders, values)

def get_tweet(tweet_pk):
    """ return a single tweet object for a given tweet ID"""
    where = "WHERE pk = ?"
    values = (tweet_pk, )
    return Tweet.select_one(where, values)

def make_tweet(pk, text):
    if len(text) > 280:
        return ValueError
    tweet = Tweet()
    tweet.account_pk = pk
    tweet.tweet_text = text
    tweet.time = get_timestamp()
    tweet.username = tweet.get_username()
    tweet.save()
    return tweet

def retweet(tweet_pk):
    tweet_orig = get_tweet(tweet_pk)
    tweet_orig.retweet_count += 1
    tweet_orig.save()
    tweet_new = make_tweet(tweet_orig.account_pk, tweet_orig.tweet_text)
    return tweet_new

def like(tweet_pk):
    tweet = get_tweet(tweet_pk)
    tweet.likes += 1
    tweet.save()
    
    # def json(self):
    #     return {"ticker": self.ticker, "volume": self.volume, "price": self.price, "time": self.time}
# print(Tweet.get_tweets_for_user(1))