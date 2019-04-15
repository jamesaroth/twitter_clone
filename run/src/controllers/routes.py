from flask import jsonify, request, render_template, url_for, redirect, session
from requests.exceptions import ConnectionError
from datetime import datetime

from src import app
from .util import hash_pass
from .account import Account
from .tweet import Tweet, make_tweet, get_tweets_for_user, get_tweet, retweet, like

UNAUTHORIZED = {"error": "unauthorized", "status_code": 401}
NOT_FOUND = {"error": "not found", "status_code": 404}
APP_ERROR = {"error": "application error", "status_code": 500}
BAD_REQUEST = {"error": "bad request", "status_code": 400}

@app.errorhandler(404)
def error404(e):
    return jsonify(NOT_FOUND), 404

@app.errorhandler(500)
def error500(e):
    return jsonify(APP_ERROR), 500

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        alltweets = Tweet.select_all_tweets()
        return render_template('login.html', alltweets=alltweets)
    elif request.method == 'POST':
        session['username'] = request.form['email_login']
        session['password'] = request.form['password_login']
        account = Account.verify(session['username'], session['password'])
        if account == None:
            alltweets = Tweet.select_all_tweets()
            return render_template('login.html', error="You've entered an invalid email/password combination.  Please try again or signup to create a new account.", alltweets=alltweets)
        usertweets = get_tweets_for_user(account.pk)
        return render_template('dashboard.html', username=session['username'], alltweets=usertweets, buttontype1="default", buttontype2="primary")
    
    else:
        return render_template('login.html', error="Something went wrong.  Please try logging in again or creating a new account")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username_try = request.form['email_signup']
        password_try = request.form['password_signup']
        password_reset_try = request.form['password_signup_confirm']

        if request.form['email_signup'] == None:
            return render_template('signup.html', error2="The passwords you've entered do not match or you already have an account or you didn't fill out the form correctly.  Please try again.")
        elif hash_pass(request.form['password_signup']) != hash_pass(request.form['password_signup_confirm']):
            return render_template('signup.html', error2="The passwords you've entered do not match or you already have an account or you didn't fill out the form correctly.  Please try again.")
        elif Account.verify(username_try, password_try) != None:
            return render_template('signup.html', error2="The passwords you've entered do not match or you already have an account or you didn't fill out the form correctly.  Please try again.")
        elif Account.select_one(where_clause="WHERE username = ?", values=(username_try,)) != None:
            return render_template('signup.html', error2="The passwords you've entered do not match or you already have an account or you didn't fill out the form correctly.  Please try again.")
        else:
            session['username'] = request.form['email_signup']
            session['password'] = request.form['password_signup']
            account = Account()
            account.username = session['username']
            account.password_hash = hash_pass(session['password'])
            account.save()
            usertweets = get_tweets_for_user(account.pk)
            return render_template('dashboard.html', username=session['username'], alltweets=usertweets, buttontype1="default", buttontype2="primary")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        account = Account.verify(session['username'], session['password'])
        usertweets = get_tweets_for_user(account.pk)
        return render_template('dashboard.html', username=session['username'], alltweets=usertweets, buttontype1="secondary", buttontype2="default")
    if request.method == 'POST':
        account = Account.verify(session['username'], session['password'])
        if request.form.get("new_tweet") != None:
            make_tweet(account.pk, request.form['new_tweet'])
            usertweets = get_tweets_for_user(account.pk)
            return render_template('dashboard.html', username=session['username'], alltweets=usertweets, buttontype1="default", buttontype2="primary")
        elif request.form.get("all_users"):
            usertweets = Tweet.select_all_tweets()
            return render_template('dashboard.html', username=session['username'], alltweets=usertweets, buttontype1="primary", buttontype2="default")
        elif request.form.get("my_users"):
            alltweets = get_tweets_for_user(account.pk)
            return render_template('dashboard.html', username=session['username'], alltweets=alltweets, buttontype1="default", buttontype2="primary")
        elif request.form.get("retweet"):
            retweet_pk = request.form['retweet']
            retweet(retweet_pk)
            alltweets = get_tweets_for_user(account.pk)
            return render_template('dashboard.html', username=session['username'], alltweets=alltweets, buttontype1="default", buttontype2="primary")
        elif request.form.get("like"):
            like_pk = request.form['like']
            like(like_pk)
            alltweets = get_tweets_for_user(account.pk)
            return render_template('dashboard.html', username=session['username'], alltweets=alltweets, buttontype1="default", buttontype2="primary")
        else:
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('password', None)
   return redirect(url_for('login'))

def convertTime(time):
    return datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')