# using:utf-8

import json
from requests_oauthlib import OAuth1Session
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
        
        """
        with open("../.token", "r") as f:
            temp = f.read().split("\n")

            self.API_KEY     = temp[0]
            self.API_SECRET  = temp[1]
            self.ACCESS_TOKEN        = temp[2]
            self.ACCESS_TOKEN_SECRET = temp[3]

            self.screen_name = screen_name
            self.url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    
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

        tweets = []
        max_id = 0

        while True:
            # 1秒待つ
            sleep(1)

            # ループした数だけ"."を出力する
            print(".", end="")

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
            
            res = twitter.get(self.url, params=params)
            dic = json.loads(res.text)
            
            if max_id == dic[-1]["id"]:
                break
            else:
                tweets += dic
                max_id = dic[-1]["id"]

        return tweets


twitter = Twitter("teriyaki398")
res = twitter.getUsersTweets()