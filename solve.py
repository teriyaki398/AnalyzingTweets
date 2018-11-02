import json
from time import sleep
from requests_oauthlib import OAuth1Session
from tqdm import tqdm
import sys

with open("../.token/TwitterToken", "r") as f:
    TOKEN = f.read().split("\n")
    TOKEN = list(map(lambda x: x.split(" "), TOKEN))[:-1]

with open("../Output/AnalyzingTweets", "r") as f:
    USER_ID = f.read().split(" ")[1][:-1]

with open("../Output/"+USER_ID+"-Followers", "r") as f:
    followers = f.read().split("\n")[:-1]

with open("../Output/"+USER_ID+"-Statistics", "r") as f:
    statis = f.read().split("\n")[:-1]
# remove searched followers
for i in statis:
    name = i.split(" ")
    if name[0] in followers:
        followers.remove(name[0])

with open("../Output/"+USER_ID+"-TWEETS", "r") as f:
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
    return ""


def getFav(name, max_id):
    # Auth
    twitter = OAuth1Session(TOKEN[0][1], TOKEN[1][1], TOKEN[2][1], TOKEN[3][1])
    # request url
    url = "https://api.twitter.com/1.1/favorites/list.json"
    # request parameters
    if max_id == -1:
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
    url = "https://api.twitter.com/1.1/users/show.json"
    params = {"screen_name": name}
    res = twitter.get(url, params=params)
    dic = json.loads(res.text)
    return dic["favourites_count"]

def writeAns(out):
    with open("../Output/"+USER_ID+"-Statistics", "a") as f:
        f.write(out[0] + " " + str(out[1]) + "\n")
    


for search_user in tqdm(followers):
    sleep(15)
    fav_cnt = getFavoritesCount(search_user)
    print("search @" + search_user)

    dic = getFav(search_user, -1)

    # private account flag
    flag = True
    try:
        dic[0]["user"]["screen_name"] == USER_ID
    except:
        flag = False
    if flag == False:
        print("Private Account...")
        print search_user, 0
        writeAns([search_user, 0])
        continue
    
    # sccess to read
    ans = []
    for i in dic:
        if retDateNum(i) < "201804010000": continue
        if i["user"]["screen_name"] == USER_ID:
            ent = i["id"]
            print "-"
            print i["created_at"]
            print i["user"]["name"]
            print i["text"]
            print "-"
            if ent not in ans:
                ans.append(ent)

    # continue to search
    max_id = retNextMaxID(dic)

    if max_id == "":
        print("Next is none...")
        print search_user, len(ans)
        writeAns([search_user, len(ans)])
        continue

    for _ in tqdm(range(fav_cnt / 200)):
        sleep(15)

        dic = getFav(search_user, max_id)
        for i in dic:
            if retDateNum(i) < "201804010000": continue
            if i["user"]["screen_name"] == USER_ID:
                ent = i["id"]
                if ent not in ans:
                    print "-"
                    print i["created_at"]
                    print i["user"]["name"]
                    print i["text"]
                    print "-"
                    ans.append(ent)
        
        if len(dic) == 0:
            "search error"
            break
        else:
            max_id = retNextMaxID(dic)
        
        if max_id == "":
            print "Date Limit..."
            break

    print search_user, len(ans)
    writeAns([search_user, len(ans)])
