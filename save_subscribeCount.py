#別ファイルをインポート
import twitter_auto_posts

def save_Count(now_count):
    #テキストファイルを読み込む
    with open("subscriberCount.txt","r") as f:
        pre_subscriberCount=f.read()

    #登録者数が変化していた場合
    if now_count!=pre_subscriberCount:
        #登録者数をツイートする
        twitter_auto_posts.count_tweet(now_count)

        #テキストファイルに書き込む
        with open("subscriberCount.txt","w") as f:
            f.write(str(now_count))