import time
from .orm import ORM
from .util import hash_pass
from .tweet import Tweet
from .hashtag import Hashtag
from datetime import datetime
import sqlite3

class Account(ORM):
    fields = ["username", "password_hash"]
    table = "accounts"

    def __init__(self):
        self.pk = None
        self.username = None
        self.password_hash = None

    def set_password(self, password):
        self.password_hash = hash_pass(password)
    
    def create_account(self, username, password_hash):
        account = Account()
        self.username = username
        self.password_hash = password_hash
        account.save()

    @classmethod
    def login(cls, username, password):
        account = cls.select_one("WHERE password_hash = ? AND username = ?", (password, username))
        if not account:
            return None
        else:    
            return account
    @classmethod
    def verify(cls, username, password):
        account = cls.select_one("WHERE password_hash = ? AND username = ?", (hash_pass(password), username))
        if not account:
            return None
        else:    
            return account
    
    # SELECT username FROM accounts WHERE accounts.pk = tweets.account_pk

#TODO
    
    def make_tweet(self, text):
        if len(text) > 280:
            return ValueError
        tweet = Tweet()
        tweet.account_pk = self.pk
        tweet.tweet_text = text
        tweet.time = time.time()
        tweet.save()
        return tweet

    def get_all_tweets(self):
        """ return a list of all Tweets in chronological order for all users"""
        return Tweet.select_all_tweets()
    
    def get_tweets(self, pk):
        """ return a list of each Tweet object for this user """
        where = "WHERE account_pk = ?"
        values = (pk, )
        return Tweet.select_many(where, values)
    
    def get_usernames(self, pk):
        
        pass

    # def get_tweets_for_hashtag(self, hashtag):
    #     """ return a list of all tweets for a given hashtag for this user """
    #     where = "WHERE account_pk = ? AND hashtag = ?"
    #     values = (self.pk, hashtag)
    #     return Tweet.select_many(where, values)

    # def get_hashtags_for_tweet(self, tweet):
    #     where = "WHERE account_pk = ? AND ticker = ?"
    #     values = (self.pk, ticker)
    #     result = Position.select_one(where, values)
    #     if result:
    #         return result

    # def make_hashtag(self, tweet)           position = self.get_position_for(ticker)
    #     position.shares += amount
    #     self.save()
    #     trade.save()
    #     position.save()

    # def sell(self, ticker, amount):
    #     price = get_price(ticker)
    #     position = self.get_position_for(ticker)
    #     if position.shares < amount:
    #         raise ValueError(
    #             "Insufficient Shares to Sell or Position Does not Exist")
    #     self.balance += price * amount
    #     trade = Trade()
    #     trade.account_pk = self.pk
    #     trade.ticker = ticker
    #     trade.price = price
    #     trade.volume = -1 * amount
    #     trade.time = time.time()

    #     position.shares -= amount
    #     self.save()
    #     trade.save()
    #     position.save()
