# from .controllers.account import Account
# from .controllers.tweet import Tweet
# from .controllers.hashtag import Hashtag

from flask import Flask, session
app = Flask(__name__)
app.secret_key = "Please Work"
from .controllers import routes
