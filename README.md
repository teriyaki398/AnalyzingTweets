# Analyzing Tweets
Twitter API ではなぜか特定のツイートに対して誰がいいねしたかを取得することができない（2018年11月現在）

愚直に自分のフォロワーを探索して行く方法があるが、尋常じゃないほど時間がかかるので、別の方法でいいねの統計をとる。

1. Twitter API で自分のツイートを全て取得
2. [こちら](https://stackoverflow.com/questions/28982850/twitter-api-getting-list-of-users-who-favorited-a-status)の手法で取得する
3. Twitter API でidに対応する screen_name を調べる
4. matplotlib で描画

結局、1 ツイート毎に1sec 待機するのでかなり時間はかかる。

# 準備
調べたいアカウントの**screen name**を調べる。

screen name とは @XXX_YYY みたいな感じのアカウント名のこと。


# グラフを描画する
```python
python graph.py
```

で実行するだけ。

screen_name : [調べたいscreen name]

filter : [除外したいいいね数の最大値]

0 ~ filter を除外したアカウントの統計を円グラフで描画する。

