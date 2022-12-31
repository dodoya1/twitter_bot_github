#別ファイルをインポート
import subscriberCount
import latest_video_url
import twitter_auto_posts
import save_subscribeCount
#モジュールをインポート
import json
from apiclient.discovery import build

def main_tweet():
    #指定したいチャンネルのID
    CHANNEL_ID="<指定したいチャンネルのID>"

    #ここからyoutube apiに関する共通部分
    with open("secret-key.json") as f:
        secret = json.load(f)
    
    API_KEY = secret["youtube"]["key"]
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=API_KEY
    )
    #ここまで共通部分

    #登録者数
    Count=subscriberCount.Count(CHANNEL_ID,youtube)

    #登録者数が変化していた場合、登録者数をツイートする別ファイルの関数を実行
    save_subscribeCount.save_Count(Count)

    #現在の時刻15分以内に投稿された最新動画のタイトルと動画のURL(judgeは、該当動画があったかどうか)
    judge,title,latest_url=latest_video_url.url(CHANNEL_ID,youtube)

    #該当動画があった場合、ツイートする
    if judge==True:
        twitter_auto_posts.new_post_tweet(title,latest_url)