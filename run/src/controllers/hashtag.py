from .orm import ORM

class Hashtag(ORM):
    fields = ['tweet_pk', 'tag'] 
    table = 'hashtags'

    def __init__(self):
        self.pk = None
        self.tweet_pk = None
        self.tag = None

    # def json(self):
    #     return {"ticker": self.ticker, "volume": self.volume, "price": self.price, "time": self.time}
