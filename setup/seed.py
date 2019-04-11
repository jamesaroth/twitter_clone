import os
import sqlite3
import time
from pathlib import Path
from twitter import Account


p = Path(__file__).parents[1]
DBFILENAME = os.path.join(p, 'run', 'src', 'controllers', 'twitterproj.db')

def seed(DBFILENAME):
    with sqlite3.connect(DBFILENAME) as conn:
        SQL = "DELETE FROM {};"
        cur = conn.cursor()
        cur.execute(SQL.format('accounts'))
        cur.execute(SQL.format('tweets'))
        cur.execute(SQL.format('hashtags'))
    #TODO
    account = Account()
    account.username = "carter"
    account.set_password(hash_pass("password"))
    # account.api_key = '0123456789abcde'
    account.save()

    account = Account()
    account.username = "james"
    account.set_password(hash_pass("password"))
    account.save()

    tweet = Tweet()
    tweet.account_pk = 1
    tweet.tweet_text("My first tweet!")
    tweet.time = time.time()
    tweet.save()

    # position = app.Position()
    # position.account_pk = 1
    # position.ticker = 'tsla'
    # position.shares = 5
    # position.save()

    # trade1 = app.Trade()
    # trade1.time = time.time() - 24 * 60 * 60
    # trade1.ticker = 'tsla'
    # trade1.account_pk = 1
    # trade1.volume = 10
    # trade1.price = app.util.get_price('tsla') - 20.0
    # trade1.save()

    # trade2 = app.Trade()
    # trade2.time = time.time()
    # trade2.ticker = 'tsla'
    # trade2.account_pk = 1
    # trade2.volume = -5
    # trade2.price = app.util.get_price('tsla') + 20.0
    # trade2.save()

if __name__ == "__main__":
    seed(DBFILENAME)
