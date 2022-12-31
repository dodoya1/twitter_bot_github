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