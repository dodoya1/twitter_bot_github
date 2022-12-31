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