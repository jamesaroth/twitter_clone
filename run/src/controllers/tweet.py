# from ..controllers.util import hash_pass
from ..controllers.orm import ORM
# from ..controllers.account import Account
import time
from datetime import datetime

class Tweet(ORM):
    fields = ['account_pk', 'tweet_text', 'time']
    table = 'tweets'

    def __init__(self):
        self.pk = None
        self.account_pk = None
        self.tweet_text = None
        self.time = None


    # def json(self):
    #     return {"ticker": self.ticker, "volume": self.volume, "price": self.price, "time": self.time}
