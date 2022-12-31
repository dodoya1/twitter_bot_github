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