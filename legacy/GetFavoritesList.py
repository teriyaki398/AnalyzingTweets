import json
from requests_oauthlib import OAuth1Session
from time import sleep
from tqdm import tqdm


with open("../.token/TwitterToken") as f:
    TOKEN = f.read().split("\n")
    TOKEN = list(map(lambda x: x.split(" "), TOKEN))[:-1]

with open("../Output/AnalyzingTweets") as f:
    USER_ID = f.read().split(" ")[1][:-1]

with open("../Output/Users_Tweets", "r") as f:
    TWEETS = f.read().split("\n")[:-1]
    TWEETS = [i.split(" ") for i in TWEETS]


MONTH = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", 
        "Jun":"06", "Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10",
        "Nov":"11", "Dec":"12"}

def retDateNum(dic):
    date = dic["created_at"].split(" ")
    return date[-1] + MONTH[date[1]] + date[2] + date[3].replace(":", "")

def retNextMaxID(dic):
    date = retDateNum(dic[-1])

    for i in TWEETS:
        if date > i[1]:
            return i[0]
            break
    return ""


def getFav(name, max_id):

    twitter = OAuth1Session(TOKEN[0][1], TOKEN[1][1], TOKEN[2][1], TOKEN[3][1])
    # request url
    url = "https://api.twitter.com/1.1/favorites/list.json"

    if max_id == -1:
        # request parameters
        params = {"screen_name": name, "count": 200}
    else:
        params = {"screen_name": name, "max_id": max_id, "count": 200}

    # request
    res = twitter.get(url, params=params)
    # json -> dict
    dic = json.loads(res.text)

    return dic


def getFavoritesCount(name):
    twitter = OAuth1Session(TOKEN[0][1], TOKEN[1][1], TOKEN[2][1], TOKEN[3][1])

    # request url
    url = "https://api.twitter.com/1.1/users/show.json"

    # request parameters
    params = {"screen_name": name}

    # request
    res = twitter.get(url, params=params)

    # json -> dict
    dic = json.loads(res.text)

    return dic["favourites_count"]

ans = []

SEARCH_USER = ""
fav_cnt = getFavoritesCount(SEARCH_USER)

dic = getFav(SEARCH_USER, -1)

for i in dic:
    if i["user"]["screen_name"] == USER_ID:
        ent = i["id"]
        if ent not in ans:
            ans.append(ent)

max_id = retNextMaxID(dic)
for _ in tqdm(range(fav_cnt / 200)):
    sleep(20)

    dic = getFav(SEARCH_USER, max_id)
    for i in dic:
        if i["user"]["screen_name"] == USER_ID:
            ent = i["id"]
            if ent not in ans:
                print(i["text"])
                print("-")
                ans.append(ent)
    
    max_id = retNextMaxID(dic)
    if max_id == "":
        break

with open("../Output/ans", "w") as f:
    for i in ans:
        f.write(str(i) + "\n")