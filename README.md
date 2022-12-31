# リポジトリの説明・概要

Youtubeの特定のチャンネルの新規動画投稿や登録者数の変化を知ることで、自分が興味を持っているチャンネルの情報をリアルタイムで知ることができるようにする。

# 使用方法

1. Twitter Developerアカウントを作成して、Twitter APIを使用するためのAPIキーとAPIシークレットを取得する。
2. Google Cloud Platformアカウントを作成して、Youtube Data API v3のAPIキーを取得する。
3. 取得したTwitter APIとYoutube Data API v3のキーやトークンを「secret-key.json」に書く。
4. 指定したい指定したいチャンネルのIDを「main.py」の変数CHANNEL_IDに代入する。
5. 必要なモジュールをインポートする。main.pyを実行し、エラーが発生したら逐次インポートすれば良い。

# 各ファイルの概要

* main.py  
    **外部ファイルを読み込み、関数を実行する**

* save_subscribeCount.py  
    **現在の登録者数をテキストファイルに書き込む**

* latest_video_url.py  
    **Youtubeの特定のチャンネルについて、最新動画のタイトルと動画のURLを取得する**

* twitter_auto_posts.py  
    **Twitter APIを使用して、Twitterに対して新規投稿や登録者数のツイートを行う**

* subscriberCount.py  
    **Youtube Data APIを使用して、特定のチャンネルの登録者数を取得する**

* secret-key.json  
    **Twitter APIとYoutube Data API v3のキーやトークン**

* subscriberCount.txt  
    **登録者数を保存する**

# 各ファイルのクラスや関数

* main.py  
    **外部ファイルを読み込み、関数を実行する**

    「main_tweet」という関数を定義しています。

    この関数内で、Youtube APIを使用して、指定したチャンネルの登録者数を取得し、登録者数が変化していた場合には、別のファイルの関数を使用して、登録者数をツイートする処理を行っています。

    また、この関数内では、指定したチャンネルについて、現在時刻15分以内に投稿された最新動画のタイトルと動画のURLを取得しています。

    最後に、該当動画があった場合には、別のファイルの関数を使用して、最新動画のタイトルと動画のURLをツイートする処理を行っています。
* save_subscribeCount.py  
    **現在の登録者数をテキストファイルに書き込む**

    「save_Count」という関数を定義しています。

    この関数には、現在の登録者数を表す「now_count」という引数があります。関数内では、まず、「subscriberCount.txt」というテキストファイルを読み込み、その内容を「pre_subscriberCount」という変数に代入しています。

    その後、現在の登録者数と、前回取得した登録者数を比較して、登録者数が変化している場合にのみ、別のファイルの関数を使用して、登録者数をツイートする処理を行っています。

    最後に、「subscriberCount.txt」というテキストファイルに、現在の登録者数を書き込んでいます。

* latest_video_url.py  
    **Youtubeの特定のチャンネルについて、最新動画のタイトルと動画のURLを取得する**

    「url」という関数を定義しています。

    この関数には、指定したチャンネルのIDを表す「CHANNEL_ID」と、Youtube APIを使用するための「youtube」という変数があります。関数内では、まず、Youtube APIを使用して、指定したチャンネルから最新の動画を1件取得します。

    その後、取得した動画のIDとタイトルを取得し、最新の動画のURLを作成します。また、取得した動画の投稿日時を取得し、それを日時型のデータに変換します。そして、コード実行日時を取得し、それも日時型のデータに変換します。

    最後に、最新動画の投稿日時が現在の時刻の15分以内かどうかを判定し、条件を満たす場合には「True」、そうでない場合には「False」を返すようにしています。

* twitter_auto_posts.py  
    **Twitter APIを使用して、Twitterに対して新規投稿や登録者数のツイートを行う**

    プログラムは、まず、「tweepy」というライブラリをインポートしています。このライブラリを使用することで、PythonからTwitter APIを使用することができます。また、「json」というライブラリをインポートしており、これを使用することで、JSON形式のファイルを読み込むことができます。そして、「datetime」というライブラリをインポートしており、これを使用することで、日付や時刻を取得したり、日付や時刻を文字列に変換したりすることができます。

    次に、プログラムでは、「secret-key.json」というファイルを開き、その中に記述されたTwitter APIのキーやトークンを読み込んでいます。そして、これらのキーやトークンを使用して、「tweepy」を使用するための「client」という変数を作成しています。

    最後に、プログラムでは、「new_post_tweet」という関数を定義しています。この関数には、動画のタイトルを表す「title」と、動画のURLを表す「latest_url」という変数があります。この関数では、本文として、動画のタイトルやURLを含めた文章をツイートするようにしています。また、「count_tweet」という関数も定義されています。この関数には、登録者数を表す「subscriberCount」という変数があります。この関数では、本文として、登録者数を表す文字列を作成し、その文字列をツイートするようにしています。

    それぞれの関数では、「client.create_tweet」というメソッドを使用して、指定された本文をツイートするようにしています。このメソッドには、本文を表す「text」という引数があります。

* subscriberCount.py  
    **Youtube Data APIを使用して、特定のチャンネルの登録者数を取得する**

    まず、youtube.channels().list()メソッドを使用して、チャンネル情報を取得しようとしています。このとき、partパラメータに'snippet,statistics'を指定しています。これは、取得する情報をスニペット(チャンネルのタイトルや説明など)と統計情報(登録者数や再生回数など)に限定することを意味します。また、idパラメータにCHANNEL_IDを指定しています。これは、取得するチャンネルを特定するためのものです。

    次に、response.get("items", [])で、itemsというキーに対応する値(チャンネル情報)を取得しています。このとき、itemsがない場合には、空のリストを返すようにしています。そして、for文で、取得したチャンネル情報を1件ずつ取り出しています。そして、kindキーが"youtube#channel"であるもののみを対象としています。これは、他のタイプのリソース(例えば、プレイリストや動画など)を除外するためです。

    最後に、channel["statistics"]["subscriberCount"]で、登録者数を取得しています。

    このプログラムを実行すると、特定のチャンネルの登録者数が取得できます。

* secret-key.json  
    **Twitter APIとYoutube Data API v3のキーやトークン**

* subscriberCount.txt  
    **登録者数を保存する**

# 各ファイルの関係

main.pyが他のファイルの関数を呼び出すなどの役目を行っています。

そのため、main.pyのmain_tweet関数を実行することで目的のbotが作動します。

```sh:main_tweet関数を実行する
python -c "import main; main.main_tweet()"
```

# 作成ステップ

[Qiitaの記事]()を見て下さい。