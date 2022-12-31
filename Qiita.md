---
title: Youtubeチャンネルの新規動画投稿と登録者数を自動通知するTwitter botを作った話
tags: YouTube API Python TwitterAPI GoogleCloudPlatform
author: oyutaka_jp
slide: false
---
# 目次
- [1. はじめに](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB)
- [2. Twitter botとは](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#twitter-bot%E3%81%A8%E3%81%AF)
- [3. Youtube Data API v3とは](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#youtube-data-api-v3%E3%81%A8%E3%81%AF)
- [4. Twitter APIとは](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#twitter-api%E3%81%A8%E3%81%AF)
- [5. Twitter botの作成手順](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#twitter-bot%E3%81%AE%E4%BD%9C%E6%88%90%E6%89%8B%E9%A0%86)
- [6. 実際に作成したTwitter botのデモ](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#%E5%AE%9F%E9%9A%9B%E3%81%AB%E4%BD%9C%E6%88%90%E3%81%97%E3%81%9Ftwitter-bot%E3%81%AE%E3%83%87%E3%83%A2)
- [7. まとめ](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#%E3%81%BE%E3%81%A8%E3%82%81)
- [8. 詰まったところ](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#%E8%A9%B0%E3%81%BE%E3%81%A3%E3%81%9F%E3%81%A8%E3%81%93%E3%82%8D)
- [9. 感想](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#%E6%84%9F%E6%83%B3)
- [10. 参考文献](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE)

# はじめに
## Twitter botの開発の目的
**Youtubeの特定のチャンネルの新規動画投稿や登録者数の変化を知る**ことで、自分が興味を持っているチャンネルの情報をリアルタイムで知ることができるようにする。

<font color="red">**Twitter botの作成手順**</font>は、概ね以下のようになります。

1. **Twitter Developerアカウントを作成**:
Twitter Developerアカウントを作成して、Twitter APIを使用するためのAPIキーとAPIシークレットを取得する。
2. **GCPアカウントを作成し、APIキーを取得する**:
Youtube Data API v3を使用して、特定のチャンネルから新しい動画を取得する。このAPIを使用するには、Google Cloud Platformアカウントを作成し、APIキーを取得する必要がある。
3. **特定のチャンネルから新しい動画を取得する**:
Youtube Data API v3を使用して、特定のチャンネルから新しい動画を取得するには、「search.list」メソッドを使用する。
4. **動画のURLをツイートする**:
新しい動画を検出したら、Twitter APIを使用し、その動画のURLをツイートする。このAPIを使用するには、APIキーとAPIシークレットを使用して、OAuth認証を行う必要がある。
5. **定期実行**:
定期的に新しい動画をチェックするように、Twitter botを設定する必要がある。これには、HerokuやGCPなどを使用することができる。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/255233/95da2576-9ec2-e9d2-efc6-dbef3fabb689.png)

本ブログで一番重要で読んで欲しい項目は、「[5. Twitter botの作成手順](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#twitter-bot%E3%81%AE%E4%BD%9C%E6%88%90%E6%89%8B%E9%A0%86)」です。

また、<font color="red">**早くコードを見たい人などは「[5. Twitter botの作成手順](https://qiita.com/oyutaka_jp/items/d263f0beab2e554314d7#twitter-bot%E3%81%AE%E4%BD%9C%E6%88%90%E6%89%8B%E9%A0%86)」から読むことをお勧めします**</font>。

## 本ブログで取り扱う内容
本ブログでは、Youtube Data API v3を使用してYoutubeのデータを取得する方法や、Twitter APIを使用してTwitterでのデータの投稿の方法、そして実際にTwitter botを作成する方法を解説します。

# Twitter botとは
Twitter botを使用することで、様々なタスクを自動化することができます。例えば、特定のハッシュタグを検索して、そのハッシュタグを含むツイートをリツイートするTwitter botや、特定のアカウントをフォローして、そのアカウントが投稿するツイートをリツイートするTwitter botなどがあります。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/255233/7ee6ae56-9d51-dad4-3225-f64f7c3feadf.png)

# Youtube Data API v3とは
## Youtube Data API v3とは何か
Youtube Data API v3とは、Youtubeのデータを取得するためのAPIです。Youtube Data API v3を使用することで、Youtubeのデータを取得したり、操作したりすることができます。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/255233/ae7ce4c3-3ee4-fb1e-24a6-2750754057b3.png)

## Youtube Data API v3を使用して取得できるデータ
Youtube Data API v3を使用することで、様々なYoutubeのデータを取得することができます。例えば、特定のチャンネルの最新動画や、特定のキーワードで検索した動画、特定のチャンネルの登録者数や、特定の動画のタイトルや再生回数などを取得することができます。

## Youtube Data API v3を使用する制限
Youtube Data API v3を使用するには、APIキーを取得して、APIを呼び出すプログラムを作成する必要があります。また、Youtube Data API v3を使用するには、一定の制限があります。例えば、1日あたりのAPIコール数や、1秒あたりのAPIコール数に制限があるため、注意する必要があります。

# Twitter APIとは
## Twitter APIとは何か
Twitter APIは、Twitterのデータを取得するためのAPIです。Twitter APIを使用することで、Twitterのデータを取得したり、操作したりすることができます。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/255233/72404a65-6864-b850-4200-3a14239bf885.png)

## Twitter APIを使用して取得できるデータ
Twitter APIを使用することで、様々なTwitterのデータを取得することができます。例えば、特定のアカウントの最新ツイートや、特定のハッシュタグで検索したツイート、特定のアカウントのフォロワー数や、特定のツイートのリツイート数などを取得することができます。

## Twitter APIを使用する制限
Twitter APIを使用するには、APIキーを取得して、APIを呼び出すプログラムを作成する必要があります。また、Twitter APIを使用するには、一定の制限があります。例えば、1日あたりのAPIコール数や、1秒あたりのAPIコール数に制限があるため、注意する必要があります。

# Twitter botの作成手順
<font color="red">**Twitter botの作成手順**</font>は、概ね以下のようになります。

1. **Twitter Developerアカウントを作成**:
Twitter Developerアカウントを作成して、Twitter APIを使用するためのAPIキーとAPIシークレットを取得する。
2. **GCPアカウントを作成し、APIキーを取得する**:
Youtube Data API v3を使用して、特定のチャンネルから新しい動画を取得する。このAPIを使用するには、Google Cloud Platformアカウントを作成し、APIキーを取得する必要がある。
3. **特定のチャンネルから新しい動画を取得する**:
Youtube Data API v3を使用して、特定のチャンネルから新しい動画を取得するには、「search.list」メソッドを使用する。
4. **動画のURLをツイートする**:
新しい動画を検出したら、Twitter APIを使用し、その動画のURLをツイートする。このAPIを使用するには、APIキーとAPIシークレットを使用して、OAuth認証を行う必要がある。
5. **定期実行**:
定期的に新しい動画をチェックするように、Twitter botを設定する必要がある。これには、HerokuやGCPなどを使用することができる。

## Twitter APIキー・Youtube Data API v3キーの取得
Twitter botを作るには、まずTwitter APIキーを取得する必要があります。Twitter Developerプラットフォームにアクセスし、アプリケーションを登録して、APIキーを取得します。

また、Youtube Data API v3キーを取得するために、GCP(Google Cloud Platform)のアカウントを作成する必要があります。Twitter APIキー、Youtube Data API v3キーを取得する手順については、以下の記事が参考になるでしょう。

https://di-acc2.com/system/rpa/9688/#:~:text=API%E3%82%AD%E3%83%BC%E3%81%A8%E3%82%B7%E3%83%BC%E3%82%AF%E3%83%AC%E3%83%83%E3%83%88%E3%82%AD%E3%83%BC,Token%26Secret%E3%81%AEGenerate%20%E3%82%92%E6%8A%BC%E4%B8%8B%E3%80%82

https://masa-engineer-blog.com/python-how-to-use-youtube-data-api-v3/

https://qiita.com/rkamikawa/items/dd1fd4c1427ece787eea

## プログラムを作成する
次に、Twitter botを作成するプログラムを作成します。

Twitter APIを呼び出すためのクライアントライブラリ(tweepy)をインストールし、Twitter APIを呼び出すプログラムを作成します。また、Youtube Data API v3も組み合わせる必要があります。

実際に作成したコードを紹介し、解説していきます。また、Githubに[コード全体](https://github.com/dodoya1/twitter_bot_github)をアップロードしています。ぜひダウンロードして使ってみてください。

コードファイルは以下のようなものがあります。1から順に紹介し、解説していきます。
1. **外部ファイルを読み込み、関数を実行する**
2. **現在の登録者数をGoogleスプレッドシートに書き込む**
3. **Youtubeの特定のチャンネルについて、最新動画のタイトルと動画のURLを取得する**
4. **Twitter APIを使用して、Twitterに対して新規投稿や登録者数のツイートを行う**
5. **Youtube Data APIを使用して、特定のチャンネルの登録者数を取得する**
6. **Twitter APIとYoutube Data API v3のキーやトークン**

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/255233/2c7863de-f9e9-7914-5ca9-65e470a84884.png)

###  外部ファイルを読み込み、関数を実行する
「main_tweet」という関数を定義しています。

この関数内で、Youtube APIを使用して、指定したチャンネルの登録者数を取得し、登録者数が変化していた場合には、別のファイルの関数を使用して、登録者数をツイートする処理を行っています。

また、この関数内では、指定したチャンネルについて、現在時刻15分以内に投稿された最新動画のタイトルと動画のURLを取得しています。

最後に、該当動画があった場合には、別のファイルの関数を使用して、最新動画のタイトルと動画のURLをツイートする処理を行っています。

```python:main.py
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
    CHANNEL_ID="<指定したいチャンネルのID(Youtube APIを使用して取得する)>"

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
```


### 現在の登録者数をGoogleスプレッドシートに書き込む
「save_Count」という関数を定義しています。

この関数には、現在の登録者数を表す「now_count」という引数があります。関数内では、まず、Youtube登録者数が書き込まれているGoogleスプレッドシートを読み込み、その内容を「pre_subscriberCount」という変数に代入しています。

その後、現在の登録者数と、前回取得した登録者数を比較して、登録者数が変化している場合にのみ、別のファイルの関数を使用して、登録者数をツイートする処理を行っています。

最後に、Googleスプレッドシートに、現在の登録者数を書き込んでいます。

```python:save_subscribeCount.py
import gspread
from google.oauth2.service_account import Credentials
import os
#別ファイルをインポート
import twitter_auto_posts

def save_Count(now_count):
    # お決まりの文句
    # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    # 実行ファイルのディレクトリパスの取得
    dir_path = os.path.abspath("<GCPでダウンロードしたJSON秘密鍵ファイル名>")
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
    credentials = Credentials.from_service_account_file(dir_path, scopes=scope)
    #OAuth2の資格情報を使用してGoogle APIにログイン。
    gc = gspread.authorize(credentials)

    #スプレッドシートIDを変数に格納する。
    SPREADSHEET_KEY = "<スプレッドシートID>"
    # スプレッドシート（ブック）を開く
    workbook = gc.open_by_key(SPREADSHEET_KEY)
    # シートを開く
    worksheet = workbook.worksheet('シート1')

    #読み込む
    pre_subscriberCount= worksheet.acell('A1').value

    #登録者数が変化していた場合
    if now_count!=pre_subscriberCount:
        #セルA1にnow_countという文字列を書き込む
        worksheet.update_cell(1,1,now_count)
        #登録者数をツイートする
        twitter_auto_posts.count_tweet(now_count)
```

### Youtubeの特定のチャンネルについて、最新動画のタイトルと動画のURLを取得する
「url」という関数を定義しています。

この関数には、指定したチャンネルのIDを表す「CHANNEL_ID」と、Youtube APIを使用するための「youtube」という変数があります。関数内では、まず、Youtube APIを使用して、指定したチャンネルから最新の動画を1件取得します。

その後、取得した動画のIDとタイトルを取得し、最新の動画のURLを作成します。また、取得した動画の投稿日時を取得し、それを日時型のデータに変換します。そして、コード実行日時を取得し、それも日時型のデータに変換します。

最後に、最新動画の投稿日時が現在の時刻の15分以内かどうかを判定し、条件を満たす場合には「True」、そうでない場合には「False」を返すようにしています。

```python:latest_video_url.py
from datetime import datetime

def url(CHANNEL_ID,youtube):
    response = youtube.search().list(
        part = "snippet",
        channelId = CHANNEL_ID,
        maxResults = 1,
        order = "date" #日付順にソート
    ).execute()

    for item in response.get("items", []):
        if item["id"]["kind"] != "youtube#video":
            continue
        video=item
    #videoId
    videoId=video["id"]["videoId"]
    #タイトル
    title=video["snippet"]["title"]
    #最新の動画の投稿日時
    publishTime=video["snippet"]["publishTime"]
    #最新の動画のURL
    latest_url=f"https://youtu.be/{videoId}"

    #コード実行日時
    now = datetime.now()
    #日付をunixtimeに変換(小数点以下切り捨て)
    now_ts = int(now.timestamp())

    #最新動画投稿日時(ISO 8601形式)
    s = publishTime
    #末尾のZを削除
    s=s[:-1]
    #日時（日付・時刻）を文字列に変換
    latest_dt = datetime.fromisoformat(s)
    #日付をunixtimeに変換(小数点以下切り捨て)
    latest_ts = int(latest_dt.timestamp())

    #最新動画投稿日時が現在の時刻の15分以内の場合(実行時間のズレを考慮し、念の為16にしておく)
    if now_ts-latest_ts<=16*60:
        return True,title,latest_url
    else:
        return False,0,0
```




### Twitter APIを使用して、Twitterに対して新規投稿や登録者数のツイートを行う
プログラムは、まず、「tweepy」というライブラリをインポートしています。このライブラリを使用することで、PythonからTwitter APIを使用することができます。また、「json」というライブラリをインポートしており、これを使用することで、JSON形式のファイルを読み込むことができます。そして、「datetime」というライブラリをインポートしており、これを使用することで、日付や時刻を取得したり、日付や時刻を文字列に変換したりすることができます。

次に、プログラムでは、「secret-key.json」というファイルを開き、その中に記述されたTwitter APIのキーやトークンを読み込んでいます。そして、これらのキーやトークンを使用して、「tweepy」を使用するための「client」という変数を作成しています。

最後に、プログラムでは、「new_post_tweet」という関数を定義しています。この関数には、動画のタイトルを表す「title」と、動画のURLを表す「latest_url」という変数があります。この関数では、本文として、動画のタイトルやURLを含めた文章をツイートするようにしています。また、「count_tweet」という関数も定義されています。この関数には、登録者数を表す「subscriberCount」という変数があります。この関数では、本文として、登録者数を表す文字列を作成し、その文字列をツイートするようにしています。

それぞれの関数では、「client.create_tweet」というメソッドを使用して、指定された本文をツイートするようにしています。このメソッドには、本文を表す「text」という引数があります。

```python:twitter_auto_posts.py
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
```

### Youtube Data APIを使用して、特定のチャンネルの登録者数を取得する
まず、youtube.channels().list()メソッドを使用して、チャンネル情報を取得しようとしています。このとき、partパラメータに'snippet,statistics'を指定しています。これは、取得する情報をスニペット(チャンネルのタイトルや説明など)と統計情報(登録者数や再生回数など)に限定することを意味します。また、idパラメータにCHANNEL_IDを指定しています。これは、取得するチャンネルを特定するためのものです。

次に、response.get("items", [])で、itemsというキーに対応する値(チャンネル情報)を取得しています。このとき、itemsがない場合には、空のリストを返すようにしています。そして、for文で、取得したチャンネル情報を1件ずつ取り出しています。そして、kindキーが"youtube#channel"であるもののみを対象としています。これは、他のタイプのリソース(例えば、プレイリストや動画など)を除外するためです。

最後に、channel["statistics"]["subscriberCount"]で、登録者数を取得しています。

このプログラムを実行すると、特定のチャンネルの登録者数が取得できます。

```python:subscriberCount.py
def Count(CHANNEL_ID,youtube):
    response = youtube.channels().list(
        part = 'snippet,statistics',
        id = CHANNEL_ID
    ).execute()

    for item in response.get("items", []):
        if item["kind"] != "youtube#channel":
            continue
        channel=item
    #登録者数
    subscriberCount=channel["statistics"]["subscriberCount"]
    
    return subscriberCount
```

### Twitter APIとYoutube Data API v3のキーやトークン

```json:secret-key.json
{
    "youtube": {
        "key" : "<取得したキー>"
    },
    "twitter": {
        "key" : "<取得したキー>",
        "secret_key" : "<取得したキー>",
        "access_token" : "<取得したトークン>",
        "access_token_secret" : "<取得したトークン>"
    }
}
```

また、プログラムを作成するには、以下の記事が参考になるでしょう。

https://masa-engineer-blog.com/python-how-to-use-youtube-data-api-v3/

https://qiita.com/rkamikawa/items/dd1fd4c1427ece787eea

https://izadori.net/python-twitter/

https://docs.oracle.com/cd/E39368_01/admin/configure-cronjobs.html

https://www.server-memo.net/tips/crontab.html

## Twitter botをデプロイする
最後に、Twitter botをデプロイします。Twitter botをデプロイする方法には、GCP(Google Cloud Platform)やHerokuなどがあります。今回は、GCP(Google Cloud Platform)上のCloud Scheduler、Cloud Functions、Cloud Pub/Subを使用しました。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/255233/fa3c7cb4-fc96-0a75-1497-71a959b791f6.png)

以下の記事が参考になるでしょう。

https://amateur-engineer-blog.com/cloud-functions-periodic-execution/

https://qiita.com/niwasawa/items/90476112dfced169c113

https://youtu.be/SuaHjAv5QJA

# 実際に作成したTwitter botのデモ
こちらが実際に作成したTwitter botです。今回私は、ラムダ技術部さんのYoutubeチャンネルの新規動画投稿と登録者数を知るTwitter botを作成しました。コードのChannel IDを変えるだけで、指定したいYoutubeチャンネルを変更することができます。ぜひ試してみて下さい。

[ラムダ技術部YouTube登録者数、動画投稿通知bot](https://twitter.com/lambdatech_bot)

# まとめ
本ブログでは、Youtubeの特定のチャンネルの新規動画投稿と登録者数が変化した場合を知らせるTwitter botを作成する方法について解説しました。特定のチャンネルの新規動画投稿を取得するには、Youtube Data API v3を使用しました。また、Twitter botを作成するには、Twitter APIを使用しました。

Twitter botを作成するには、Twitter APIキーを取得して、プログラムを作成し、デプロイする必要があります。Twitter APIキーを取得するには、Twitter Developerプラットフォームにアクセスし、アプリケーションを登録する必要があります。
プログラムを作成するには、Twitter APIを呼び出すためのクライアントライブラリをインストールし、Twitter APIを呼び出すプログラムを作成する必要があります。デプロイするには、Cloud FunctionsやHerokuなどが利用できます。

# 詰まったところ
* 「requirements.txt」には、google-api-python-client==1.9.3と書く必要があります。
* 実行したい関数には、必ず「event, content」という引数を指定する必要があります。この問題が原因でエラーが発生し、ほとんどの時間をこの問題の解決に費やしました。
* tweepyでは、短時間で全く同じ文章をツイートしようとすると、ツイートが拒否されるようになっています。そのため、実行日時をツイート本文に入れるようにして、全く同じ内容のツイートにしないように変更しました。

# 感想
* コードはすぐに出来たが、GCPの設定やAPI側の決まり事に関するエラーが発生し、それを一つ一つ解決するのに時間がかかり、疲れた。
* 最初は15分ごとにYoutube登録者数をツイートするコードを書いていたが、Youtube登録者数が変化したときだけツイートするように変更した。この変更は良い改善だと思う。
* GCPやjsonファイルやテキストファイルを初めて扱った。そのために色々調べて勉強することで技術力が上がり、面白かった。
* 改めてエラーコードをじっくりと読む大切さを痛感した。

# 参考文献
## 特に参考になったもの
https://di-acc2.com/system/rpa/9688/#:~:text=API%E3%82%AD%E3%83%BC%E3%81%A8%E3%82%B7%E3%83%BC%E3%82%AF%E3%83%AC%E3%83%83%E3%83%88%E3%82%AD%E3%83%BC,Token%26Secret%E3%81%AEGenerate%20%E3%82%92%E6%8A%BC%E4%B8%8B%E3%80%82

https://masa-engineer-blog.com/python-how-to-use-youtube-data-api-v3/

https://qiita.com/rkamikawa/items/dd1fd4c1427ece787eea

https://note.nkmk.me/python-datetime-isoformat-fromisoformat/

https://magazine.techacademy.jp/magazine/18811

https://qiita.com/shuntaro_tamura/items/5a92c517a7d95d655505

https://izadori.net/python-twitter/

https://docs.oracle.com/cd/E39368_01/admin/configure-cronjobs.html

https://www.server-memo.net/tips/crontab.html

https://amateur-engineer-blog.com/cloud-functions-periodic-execution/

https://qiita.com/niwasawa/items/90476112dfced169c113

https://youtu.be/SuaHjAv5QJA

https://osaka-se81.work/python-twitter/

https://www.javadrive.jp/python/file/index2.html

## その他
https://www.true-fly.com/entry/2021/08/26/070000

https://system.blog.uuum.jp/entry/2022/11/28/110000

# 追記
* GCP上ではテキストファイルへの書き込みは不可であったため、Googleスプレッドシート操作に変更しました。

https://www.teijitaisya.com/python-gsheets/#:~:text=%E2%96%BC%E3%83%96%E3%83%A9%E3%82%A6%E3%82%B6%E3%81%A7%E3%82%B9%E3%83%97%E3%83%AC%E3%83%83%E3%83%89%E3%82%B7%E3%83%BC%E3%83%88,%E6%9B%B8%E3%81%8D%E8%BE%BC%E3%82%80%E8%A8%AD%E5%AE%9A%E3%81%AF%E7%B5%82%E3%82%8F%E3%82%8A%E3%81%A7%E3%81%99%E3%80%82

https://noitalog.tokyo/python-google-sheets-api/
