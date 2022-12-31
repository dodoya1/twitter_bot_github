import tweepy
import json
import datetime

with open("secret-key.json") as f:
    secret = json.load(f)

consumer_key =secret["twitter"]["key"]
consumer_secret =secret["twitter"]["secret_key"]
access_token=secret["twitter"]["access_token"]
access_token_secret =secret["twitter"]["access_token_secret"]

client = tweepy.Client(
    consumer_key = consumer_key,
    consumer_secret = consumer_secret,
    access_token = access_token,
    access_token_secret = access_token_secret
)

#新規投稿
def new_post_tweet(title,latest_url):
    # ツイート本文
    text = f"""
    #ラムダ技術部 が動画を投稿しました。\n
    {title}\n
    {latest_url}\n
    {latest_url}
    """

    #ツイートする
    client.create_tweet(text = text)

#登録者数
def count_tweet(subscriberCount):
    count="{:,}".format(int(subscriberCount))

    #現在時刻
    dt_now = datetime.datetime.now()
    dt_now_format=dt_now.strftime('%Y年%m月%d日 %H時%M分')

    # ツイート本文
    text = f"""
    #ラムダ技術部 チャンネルの登録者数は{count}人です({dt_now_format}時点)。
    """

    #ツイートする
    client.create_tweet(text = text)