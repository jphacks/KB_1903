import tweepy
import urllib
import os
from flask import Flask, redirect, url_for, render_template,request,flash
import config
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl

import twitter

app = Flask(__name__)
ck = config.tw_ck
cs = config.tw_cs
auth = tweepy.OAuthHandler(ck, cs)

app.secret_key = config.secret_key #Flashのために必要

@app.route("/")
def INDEX():
    return render_template("index.html")

@app.route('/regit')
def main():
      try:
          redirect_url = auth.get_authorization_url()
          # return render_template("index.html", redirect_url=redirect_url)
          return redirect(redirect_url)
      except tweepy.TweepError:
          flash('認証に失敗しました。もう一度やり直してください。')
          return render_template("error.html")

      # return render_template("index.html", redirect_url=redirect_url)

@app.route('/callback')
def callback():
    try:
        token = request.values.get('oauth_token', '')
        verifier = request.values.get('oauth_verifier', '')
        #flash('認証に成功しました。')

        return render_template("callback.html", token=token, verifier=verifier)
    except Exception as e:
        print("callback error",e)
        return render_template("error.html")

@app.route('/input', methods=["POST"])
def input():
    if request.method == "POST":
        text = request.form["text"]
        token = request.form["token"]
        verifier = request.form["verifier"]

        auth.request_token = {'oauth_token':token, 'oauth_token_secret':verifier}
        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            print('Erroredirect Failed to get access token.')

        AT = auth.access_token
        AS = auth.access_token_secret

        twitter.twitter_fav(text,AT,AS)

        flash(text + 'を含むツイートにいいねをつけました。')
        return redirect("https://twi-api-test.herokuapp.com/")

@app.route("/start")
def startCollect():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)