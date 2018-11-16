import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from Twitter import Twitter


"""
screen name (@XXXXX ってやつ) を入力すると
円グラフが表示されるようにしたい
"""

# 対象のscreen_name
# filter : 0 ~ filter までの値は取り除く
screen_name = input("screen name : ")
filter = int(input("filter : "))

# Twitter.aggregateID()を実行。
# {ユーザーid: いいねした数} のリストが返ってくる
twitter = Twitter(screen_name)
res = twitter.aggregateID(filter)

# ユーザーid -> screen_name に変換
# いいねの数で順番にソートする
statis = [[twitter.showUser(id), res[id]] for id in res]
statis = sorted(statis, key=lambda x: x[1])

# label と data を作成する
label = []
data = []
for i in statis:
    # 自分が含まれているならば取り除く
    if i[0] == screen_name:
        continue
    else:
        label.append(i[0])
        data.append(i[1])

# 降順に直す
label = label[::-1]
data = data[::-1]

legends = ["%3d : @%s" % (data[i], label[i]) for i in range(len(label))]

plt.style.use("ggplot")
plt.rcParams.update({"font.size": 15})

size = (10,8)
temp = cm.Pastel1(np.arange(9))
col = []
for i in range(len(data)):
    col.append(temp[i % 9])

plt.figure(figsize=size, dpi=100)

plt.pie(data, colors=col, counterclock=False, startangle=90, autopct=lambda p:'{:.1f}%'.format(p) if p>=5 else '')

plt.subplots_adjust(left=0, right=0.7)
plt.legend(legends, fancybox=True, loc="center left", bbox_to_anchor=(0.9,0.5))
plt.axis("equal")
plt.savefig("./"+screen_name+"-figure.png", bbox_inches="tight", pad_inches=0.05)


