# Analyzing Tweets
最近、Twitter のいいね機能の廃止が検討されている。

ということで、今のうちに今まで自分がもらったいいね元アカウントのデータを統計で残しておきたい。

ただし、Twitter API ではなぜか特定のツイートに対して誰がいいねしたかを取得することができない（2018年11月現在）

愚直に自分のフォロワーを探索して行く方法があるが、尋常じゃないほど時間がかかるので、別の方法でいいねの統計をとる。

1. 自分のツイートを全て取得
2. [こちら](https://stackoverflow.com/questions/28982850/twitter-api-getting-list-of-users-who-favorited-a-status)の手法で取得する

サーバーへ負荷を与えないように、1sec 間隔でアクセスを行なっている。なので結局、`自分のツイート数 x 1 [sec]` の時間がかかってしまう。

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

