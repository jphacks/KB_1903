import tweepy
from flask import Flask, redirect, url_for, render_template,request,flash
import Data_analy
####



from multiprocessing import Process

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, )

import Data_analy as data
import config
from DataBase.DB_apps import DB_line


url="https://ba8a4c63.ngrok.io"




DB = DB_line()

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN
CHANNEL_SECRET = config.LINE_CHANNEL_SECRET

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
GropeDict = {}
import queue

q = queue.Queue()

# @app.route("/")
# def hello_world():
#     return "THIS IS LINE BOT"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# import web_api.weather
import requests

def get_today_Weather(**kwargs)->str:
    id="280010"
    url = f'http://weather.livedoor.com/forecast/webservice/json/v1?city={id}'
    api_data = requests.get(url).json()
    #print(api_data['title'])
    ## for weather in api_data['forecasts']:
    #     weather_date = weather['dateLabel']
    #     weather_forecasts = weather['telop']
    #     print(weather_date + ':' + weather_forecasts)
    weather=max_temp=min_temp=None
    try:
        weather=api_data["forecasts"][0]["telop"]
        max_temp=api_data["forecasts"][0]["temperature"]["max"]["celsius"]
        min_temp = api_data["forecasts"][0]["temperature"]["min"]["celsius"]
    except:
        pass
    finally:
        return weather,max_temp,min_temp

userState={}
userId_tw={}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # group か　個人かを判定
    isGroup = (event.source.type == "group")
    # print(isGroup)
    # print(event)
    user_id = event.source.user_id
    msg_t = str(event.message.text)

    if isGroup:
        GroupId = event.source.group_id

        global GropeDict
        try:
            GropeDict[GroupId] += [user_id]
            GropeDict[GroupId] = list(set(GropeDict[GroupId]))

        except:
            GropeDict[GroupId] = [user_id]

        # リクエストか
        if msg_t in ["リクエスト", "バルス"]:

            GroupId = event.source.group_id
            print(GroupId)
            # グループの各ユーザIDを取得
            #     users=line_bot_api.get_group_member_ids(GroupId)
            ##現在把握している（発言した）ユーザの趣向を出す。
            # print(type(users),users)
            userhobby = []
            ##DBに一人一人のユーザ趣向を問い合わせ
            # for u in GropeDict[GroupId]:
                # userhobby.append(DB.get_talk_his_table_from_userId(u))
            dbd=DB.get_talk_his_table(True)
            userhobby=Data_analy.countWords(dbd)
            userhobby=userhobby[0]
            # userhobby = list(set(userhobby))
            # print("userhobby::", userhobby)
            # userhobby = ",".join(userhobby)
            LineSender(line_bot_api).sendMessage(text=userhobby+"をおすすめすると話題になるかもしれません。", user_id=GroupId)
            return
    #個人
    else:
        if msg_t=="tw_get":
            userState[user_id]="q:t"
            LineSender(line_bot_api).sendMessage(text="@から始まるTwitterIDを教えてね",user_id=user_id)
            return
        elif "@" in msg_t and userState[user_id]=="q:t":
            userState[user_id]=None
            userId_tw[user_id]=msg_t
            LineSender(line_bot_api).sendMessage(text="OK!次のURLから連携してね",user_id=user_id)
            LineSender(line_bot_api).sendMessage(text=url+"/twitter-regit",user_id=user_id)
            return
    print(user_id)
    for w in Data_analy.wordAnyly(msg_t):
        DB.set_talk_history(user_id,text=w)

    # msg_t = str(event.message.text)
    #print(msg_t)
    # print(type(event))
    # user_id = event.source.user_id
    # profile = line_bot_api.get_profile(user_id)

    # status = (profile.status_message)

    # print(profile.display_name,msg_t)

    # msg = TextMessage(text=f"name::{profile.display_name}\n"
    # f"status_message::{status}")
    # weather,max_temp,min_temp=get_today_Weather()
    # msg=f"今日の天気は,{weather}\n" \
    #     f"最高気温は{max_temp}℃です。\n" \
    #     f"最低気温は{min_temp}℃です." \

    # user=LineUser(userId=user_id)
    # DB.set_new_user(user_id, user.name)
    # words = data.analy(msg_t)
    msg = "DBに保存しました"+msg_t
    LineSender(line_bot_api).sendMessage(str(msg),user_id)


    # msg_t=TextMessage(text=msg)
    # msg2=TextMessage(text=str(user))
    # for r in range(10):
    # line_bot_api.push_message(user_id, msg_t)
    # line_bot_api.push_message(user_id, msg2)
    # line_bot_api.push_message(user_id, msg_t)


def q_put(q, msg):
    q.put(msg)





class LineUser:
    def __init__(self,reply=None,userId=None):
        '''line のユーザ情報クラス　ここではreplayからUserIdを取得することも
            できるし、そのままuserIdを入力できる。
            そこからLine APIを通して、名前と　ひとこと（status message）を取得する。
        '''

        #reply か　userIdどちらも情報がない場合,userIdはNone とする。
        if  (reply or userId):
            ##replyからuserIdを取得
            if reply:
                self.userId = reply.source.user_id
            else:
                self.userId=userId
            #replyから名前とひとことを取得
            profile = line_bot_api.get_profile(self.userId)
            self.status = (profile.status_message)
            self.name=profile.display_name
        else:
            self.userId=None
            self.name=None
            self.status=None

    def __eq__(self, other):
        if type(other)==LineUser:
            return self.userId == other.userId
        else:
            return self.userId== other

    def __str__(self):
        return f"userId::{self.userId}\n" \
            f"userName::{self.name}\n" \
            f"userStatus::{self.status}"


class LineSender:
    def __init__(self,lineins:LineBotApi):
        self.line_bot_api=lineins

    def sendMessage(self,text:str,user_id:LineUser):
        if isinstance(user_id,LineUser):
            user_id=user_id.userId
        msg=TextMessage(text=text)
        self.line_bot_api.push_message(to=user_id,messages=msg)



############################ HTML TWITTER SERVER ############################
import twitter

ck = config.tw_ck
cs = config.tw_cs
auth = tweepy.OAuthHandler(ck, cs)

app.secret_key = config.tw_secret_key #Flashのために必要

@app.route("/")
def tw_INDEX():
    return render_template("index_.html")

@app.route('/twitter-regit')
def tw_main():
    try:
        redirect_url = auth.get_authorization_url()
        print("tw regit")
        # return render_template("index.html", redirect_url=redirect_url)
        return redirect(redirect_url)
    except tweepy.TweepError  as r:
        flash('認証に失敗しました。もう一度やり直してください。')
        print(r.reason)
        return render_template("error.html")

    # return render_template("index.html", redirect_url=redirect_url)

@app.route('/twitter-callback')
def tw_callback():
    try:
        token = request.values.get('oauth_token', '')
        verifier = request.values.get('oauth_verifier', '')
        flash('認証に成功しました。しばらくお待ちください')


        #################
        auth.request_token = {'oauth_token':token, 'oauth_token_secret':verifier}
        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            print('Erroredirect Failed to get access token.')

        # AT = auth.access_token
        # AS = auth.access_token_secret

        api=tweepy.API(auth,wait_on_rate_limit=False)
        # ScreenName;
        print(api.me())
        for favorite in tweepy.Cursor(api.favorites).items(50):
            # Basic information about the user who created the tweet that was favorited
            # print('\n\n\nTweet Author:')
            # # Print the screen name of the tweets auther
            # print('Screen Name: ' + str(favorite.user.screen_name.encode("utf-8")))
            # print('Name: ' + str(favorite.user.name.encode("utf-8")))
            #
            # # Basic information about the tweet that was favorited
            # print('\nTweet:')
            # # Print the id of the tweet the user favorited
            # print('Tweet Id: ' + str(favorite.id))
            # # Print the text of the tweet the user favorited
            print('Tweet Text: ' + str(favorite.text.encode("utf-8")))

        # for tweet in tweepy.Cursor(api.user_timeline, screen_name="取得したい垢名をここに入れる", exclude_replies=True).items():
        #     tweet_data.append(
        #         [tweet.id, tweet.created_at, tweet.text.replace('\n', ''), tweet.favorite_count, tweet.retweet_count])

        # ################
    except:
        return render_template("callback.html", token=token, verifier=verifier)
        # except Exception as e:
        # print("callback error",e)
        # return render_template("error.html")

# @app.route('/tw/<id>')
# def tw_callback(id):
#     try:
#         # token = request.values.get('oauth_token', '')
#         # verifier = request.values.get('oauth_verifier', '')
#         #flash('認証に成功しました。')
#
#         token="YgcasAAAAAABAX3zAAABbeaxN6E"
#         verifier="CyXOWyFrwcRb3KLBCpqMkbXoDLTuUtZW"
#
#         #################
#         auth.request_token = {'oauth_token':token, 'oauth_token_secret':verifier}
#         try:
#             auth.get_access_token(verifier)
#         except tweepy.TweepError:
#             print('Erroredirect Failed to get access token.')
#
#         AT = auth.access_token
#         AS = auth.access_token_secret
#
#         api=tweepy.API(auth,wait_on_rate_limit=False)
#         # ScreenName;
#         print(api.me())
#         for favorite in tweepy.Cursor(api.favorites,id=id).items(20):
#             # Basic information about the user who created the tweet that was favorited
#             print('\n\n\nTweet Author:')
#             # Print the screen name of the tweets auther
#             print('Screen Name: ' + str(favorite.user.screen_name.encode("utf-8")))
#             print('Name: ' + str(favorite.user.name.encode("utf-8")))
#
#             # Basic information about the tweet that was favorited
#             print('\nTweet:')
#             # Print the id of the tweet the user favorited
#             print('Tweet Id: ' + str(favorite.id))
#             # Print the text of the tweet the user favorited
#             print('Tweet Text: ' + str(favorite.text.encode("utf-8")))
#
#         # ################
#     except:
#         pass
#
#         return render_template("callback.html", token=token, verifier=verifier)
#     # except Exception as e:
#     #     print("callback error",e)
#     #     return render_template("error.html")
#




@app.route("/users/<username>")
def createHTML(username):
    ## todo databese から趣味、アイコン、名前、sns,取得
    iconURL=sns=hobby="None"
    try:
        userid=DB.get_id(username)
        hobby=DB.get_talk_his_table_from_userId(userid)
    except:
        pass

    # hobby=['アメリカフットボール', 'けもフレ']
    # # hobby=",".join(hobby)
    # iconURL="https://booth.pximg.net/0e273b68-3273-49c3-8e2b-90672b1ea0cc/i/487672/ff1c97aa-1775-4320-8a5e-6a7cbabf2460_base_resized.jpg"
    twitter="https://twitter.com/ユーザー名"
    facebook="https://twitter.com/ユーザー名"
    google_plus="https://twitter.com/ユーザー名"
    tumblr="https://twitter.com/ユーザー名"
    youtube="https://twitter.com/ユーザー名"

    return render_template("meishi.html",icon_img=iconURL,user_name=username,hobby_list=hobby,
                           twitter=twitter,google_plus=google_plus,facebook=facebook,youtube=youtube)


@app.route('/input', methods=["POST"])
def tw_input():
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

        api=tweepy.API(auth,wait_on_rate_limit=False)
        # ScreenName;
        print(api.me())
        tweepy.Cursor(api.favorites)
        twitter.twitter_fav(text,AT,AS)

        flash(text + 'を含むツイートにいいねをつけました。')
        return redirect("https://twi-api-test.herokuapp.com/")

def get_goodTweet():

    pass
def _args():
    app.run(debug=False, host='0.0.0.0', port=5000)


def start():
    s = Process(target=_args)
    s.start()
    return q



if __name__ == "__main__":
    q = start()

    # # app.run(debug=True, host='0.0.0.0', port=5000)
    # userId="U8c8b0e06213c94bc4c7f42cac57cf1a7"
    # user=LineUser(userId=userId)
    # sender=LineSender(line_bot_api)

    while 1:
        #     sender.sendMessage(text=str(user),user_id=user)
        #
        pass
