# from ..controllers.util import hash_pass
import time
from datetime import datetime

from .orm import ORM
from .account import Account

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

class Post(ORM):
    fields = ['account_pk', 'username', 'picture', 'post_text', 'time', 'repost_count', 'likes']
    table = 'posts'

    def __init__(self):
        self.pk = None
        self.account_pk = None
        self.post_text = None
        self.time = None
        self.username = None
        self.picture = None
        self.repost_count = 0
        self.likes = 0

    def get_username(self):
        user = Account.from_pk(self.account_pk)
        self.username = user.username
        return user.username

def get_posts_for_user(account_pk):
    """ return a list of each post object for this user """
    where = "WHERE account_pk = ?"
    values = (account_pk, )
    orders = "ORDER BY time DESC"
    return Post.select_many(where, orders, values)

def get_post(post_pk):
    """ return a single post object for a given post ID"""
    where = "WHERE pk = ?"
    values = (post_pk, )
    return Post.select_one(where, values)

def make_post(pk, text, imagefile):
    if len(text) > 280:
        return ValueError
    post = Post()
    post.account_pk = pk
    post.post_text = text
    post.picture = imagefile
    post.time = get_timestamp()
    post.username = post.get_username()
    post.save()
    return post

def repost(post_pk):
    post_orig = get_post(post_pk)
    post_orig.repost_count += 1
    post_orig.save()
    post_new = make_post(post_orig.account_pk, post_orig.post_text, post_orig.picture)
    return post_new

def like(post_pk):
    post = get_post(post_pk)
    post.likes += 1
    post.save()
    
    # def json(self):
    #     return {"ticker": self.ticker, "volume": self.volume, "price": self.price, "time": self.time}
# print(post.get_posts_for_user(1))