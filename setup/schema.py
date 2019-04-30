import os
from pathlib import Path
import sqlite3

p1 = Path(__file__).resolve()
p = p1.parents[1]
DBFILENAME = os.path.join(p, 'run', 'src', 'controllers', 'insta.db')

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

        SQL = """ DROP TABLE IF EXISTS posts; """
        cur.execute(SQL)

        SQL = """
        CREATE TABLE posts (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            account_pk INTEGER,
            username VARCHAR(280),
            picture BLOB,
            post_text VARCHAR(280),
            time FLOAT,
            repost_count INTEGER,
            likes INTEGER,
            FOREIGN KEY(account_pk) REFERENCES accounts(pk),
            FOREIGN KEY(username) REFERENCES accounts(username)
        ); """
        cur.execute(SQL)

        # SQL = """ DROP TABLE IF EXISTS hashtags; """
        # cur.execute(SQL)

        # SQL = """
        # CREATE TABLE hashtags (
        # pk INTEGER PRIMARY KEY AUTOINCREMENT,
        # tweet_pk INTEGER,
        # tag VARCHAR(280),
        # FOREIGN KEY(tweet_pk) REFERENCES tweets(pk)
        # ); """
        # cur.execute(SQL)
        

if __name__ == "__main__":
    create_db(DBFILENAME)
