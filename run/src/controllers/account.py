import sqlite3
import os
from datetime import datetime
import time

from .orm import ORM
from .util import hash_pass
# from .tweet import Tweet
# from .hashtag import Hashtag

class Account(ORM):
    fields = ["username", "password_hash"]
    table = "accounts"

    def __init__(self):
        self.pk = None
        self.username = None
        self.password_hash = None

    def set_password(self, password):
        self.password_hash = hash_pass(password)

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
    
    # def get_tweets_with_users(self):
    #     return Tweet.select_all_users_from_tweets()
   
   

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
# def select_all_users_from_tweets():
#         """ provide a WHERE clause to a SELECT statement and return objects
#         representing each matched row """
#         with sqlite3.connect(os.path.join(os.path.dirname(__file__), 'twitterproj.db')) as conn:
#             conn.row_factory = sqlite3.Row
#             cur = conn.cursor()
#             SQLPATTERN = "SELECT accounts.username, tweets.tweet_text, tweets.time FROM tweets INNER JOIN accounts ON accounts.pk=tweets.account_pk ORDER BY time DESC;"
#             SQL = SQLPATTERN
#             cur.execute(SQL)
#             return cur.fetchall()

