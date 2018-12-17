#using:utf-8

import json
import urllib.request, urllib.error
import re
from requests_oauthlib import OAuth1Session
from tqdm import tqdm
from time import sleep

class Twitter:
    """
    Twitter API を用いて、自分がどれだけいいねされたかを調べる
    APIを使うには TOKEN などを発行する必要がある

    screen_name : string
        対象となるユーザーの screen_name
    """

    def __init__(self, screen_name):
        """
        各情報の初期化
        認証情報は 安全のため一つ上の階層にファイルで保存した。

        screen_name : string
            引数で受け取るユーザー名

        user_timeline_url : string
            screen_name のユーザーのツイート一覧にアクセスするためのURL

        user_show_url : string
            id と screen_name を紐づけるためのURL
        """

        with open("../.token", "r") as f:
            temp = f.read().split("\n")

        self.API_KEY     = temp[0]
        self.API_SECRET  = temp[1]
        self.ACCESS_TOKEN        = temp[2]
        self.ACCESS_TOKEN_SECRET = temp[3]

        self.screen_name = screen_name
        self.user_timeline_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        self.user_show_url = "https://api.twitter.com/1.1/users/show.json"
    
    def getUsersTweets(self):
        """
        self.screen_name で指定されているユーザーのツイートを全件取得する
        辞書のリストで返す
        """

        twitter = OAuth1Session(
            self.API_KEY, 
            self.API_SECRET, 
            self.ACCESS_TOKEN, 
            self.ACCESS_TOKEN_SECRET)

        # 取得したツイートを格納するリスト
        # max_id は 0 で初期化
        tweets = []
        max_id = 0
        cnt = 0

        # ループで全てのツイートを取得する
        print("get " + self.screen_name + "\'s tweets")
        while True:
            # 1秒待つ
            sleep(1)

            # ループした数だけ"."を出力する
            print("." * (cnt+1))
            cnt += 1

            # 最初は max_id を指定しないでrequestを送る
            if max_id == 0:
                params = {
                    "screen_name": self.screen_name,
                    "count": 200
                }
            else:
                params = {
                    "screen_name": self.screen_name,
                    "count": 200,
                    "max_id": max_id
                }
            
            # APIにリクエストを送る
            try:
                res = twitter.get(self.user_timeline_url, params=params)
                dic = json.loads(res.text)
            except:
                break

            # もしmax_id が前回のものと同じなら最後まで読んだことになる
            # その時は break する
            if max_id == dic[-1]["id"]:
                break
            # そうでない場合は max_id を更新して次のループへ
            else:
                tweets += dic
                max_id = dic[-1]["id"]

        return tweets


    def getUserIDList(self,post_id):
        """
        指定されたIDのツイートにいいねした人のIDリストを返す

        id : string
            調べる ツイートID
        """
        # 一秒まつ
        sleep(1)
        
        try:
            json_data = urllib.request.urlopen(url='https://twitter.com/i/activity/favorited_popup?id=' + str(post_id)).read().decode("utf-8")
            found_ids = re.findall(r'data-user-id=\\"+\d+', json_data)
            unique_ids = list(set([re.findall(r'\d+', match)[0] for match in found_ids]))
            return unique_ids
        except urllib.request.HTTPError:
            return False
    
    def showUser(self, id):
        """
        引数で受け取ったID のユーザーの screen_name を返す

        id : string
            ユーザーID
        """
        # 一秒待つ
        sleep(1)

        twitter = OAuth1Session(
            self.API_KEY, 
            self.API_SECRET, 
            self.ACCESS_TOKEN, 
            self.ACCESS_TOKEN_SECRET)

        params = {
            "user_id": id
        }

        # APIにリクエストを送る
        try:
            res = twitter.get(self.user_show_url, params=params)
            dic = json.loads(res.text)
        except:
            return False
        
        return dic["screen_name"]


    def aggregateID(self, filter):
        """
        自分のツイートが、どのIDが何回"いいね”されたかを集計する
        
        {ユーザーid: いいねした数}
        の辞書のリストを返す

        filter : int
            合計いいね数が filter 以下のユーザーIDは除外する
        """

        # 全てのツイートの ID だけのリストを取得する
        tweets = self.getUsersTweets()
        ids = [i["id"] for i in tweets]

        # {id : いいね数} を格納する辞書
        user_ids = {}
        
        # ツイートid 一つずつ検索してく
        for id in tqdm(ids):
            lis = self.getUserIDList(id)
            # もし error が返ってきたら。
            if lis == False:
                sleep(10)
                lis = self.getUserIDList(id)
            # それでもダメなら諦めて次のやつに行く
            if lis == False:
                continue
            for i in lis:
                if i in user_ids:
                    user_ids[i] += 1
                else:
                    user_ids[i] = 1

        # フィルター以下のいいね数のデータは除外する
        # ついでに自分も除外する
        ans = {}
        for i in user_ids:
            if user_ids[i] <= filter:
                continue
            else:
                ans[i] = user_ids[i]
        return ans
