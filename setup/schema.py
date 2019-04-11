import os
from pathlib import Path
import sqlite3

p = Path(__file__).parents[1]
DBFILENAME = os.path.join(p, 'run', 'src', 'controllers', 'twitterproj.db')

def create_db(dbfilename=DBFILENAME):
    with sqlite3.connect(dbfilename) as conn:
        cur = conn.cursor()

        SQL = """ DROP TABLE IF EXISTS accounts; """
        cur.execute(SQL)

        SQL = """
        CREATE TABLE accounts (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(255),
            password_hash VARCHAR(128)
        ); """
        cur.execute(SQL)

        SQL = """ DROP TABLE IF EXISTS tweets; """
        cur.execute(SQL)

        SQL = """
        CREATE TABLE tweets (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            account_pk INTEGER, 
            tweet_text VARCHAR(280),
            time FLOAT,
            FOREIGN KEY(account_pk) REFERENCES accounts(pk)
        ); """
        cur.execute(SQL)

        SQL = """ DROP TABLE IF EXISTS hashtags; """
        cur.execute(SQL)

        SQL = """
        CREATE TABLE hashtags (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        tweet_pk INTEGER,
        tag VARCHAR(280),
        FOREIGN KEY(tweet_pk) REFERENCES tweets(pk)
        ); """
        cur.execute(SQL)
        
        SQL = """ DROP TABLE IF EXISTS tweets_hashtags; """
        cur.execute(SQL)

        SQL = """
        CREATE TABLE tweets_hashtags (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        tweet_pk INTEGER,
        hashtag_pk INTEGER,
        FOREIGN KEY(tweet_pk) REFERENCES tweets(pk), 
        FOREIGN KEY(hashtag_pk) REFERENCES hashtags(pk)
        ); """
        cur.execute(SQL)

if __name__ == "__main__":
    create_db(DBFILENAME)
