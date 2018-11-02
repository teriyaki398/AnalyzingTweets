# Analyzing Tweets

#### solve.py
自分のツイートにいいねしたアカウントの統計をとる

対象アカウントは自分のフォロワーのみ  
アカウントのリストはGetFollowers.pyで出力される

#### GetFollowers.py
自分のフォロワーリストを出力する


#### GetFavoritesList.py
いいねしたツイートのツイート主を取得する

#### GetUsersTweets.py
ユーザーの投稿したツイートを取得する

#### graph.py
取得した統計をグラフ化する


# 使い方
1. ../Output/AnalyzingTweets ファイルに
user_id [id]

という感じでTwitterのIDを指定．
このIDを元にのちの作業が行われる

2. GetFollowers.py を実行し，../Output/[ID]-Followres ファイルを作成

3. GetUsersTweets.py を実行し，../Output[ID]-TWEETS を作成

4. solve.py を実行すると，[ID]-Statisticsに結果が格納されていく

5. graph.py で結果を描画する
