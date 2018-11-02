import json
from requests_oauthlib import OAuth1Session
from time import sleep
from tqdm import tqdm


with open("../.token/TwitterToken") as f:
    TOKEN = f.read().split("\n")
    TOKEN = list(map(lambda x: x.split(" "), TOKEN))[:-1]

with open("../Output/AnalyzingTweets") as f:
    USER_ID = f.read().split(" ")[1][:-1]


MONTH = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", 
        "Jun":"06", "Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10",
        "Nov":"11", "Dec":"12"}

def retDateNum(dic):
    date = dic["created_at"].split(" ")
    return date[-1] + MONTH[date[1]] + date[2] + date[3].replace(":", "")
   



def getFav(name):

    twitter = OAuth1Session(TOKEN[0][1], TOKEN[1][1], TOKEN[2][1], TOKEN[3][1])

    # request url
    url = "https://api.twitter.com/1.1/favorites/list.json"

    # request parameters
    params = {"screen_name": name, "count": 200}

    # request
    res = twitter.get(url, params=params)

    # json -> dict
    dic = json.loads(res.text)

    return dic

def getFavWithID(name, id):
    twitter = OAuth1Session(TOKEN[0][1], TOKEN[1][1], TOKEN[2][1], TOKEN[3][1])

    # request url
    url = "https://api.twitter.com/1.1/favorites/list.json"

    # request parameters
    params = {"screen_name": name, "max_id": id, "count": 200}

    # rewuest
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


SEARCH_USER = ""
c = getFavoritesCount(SEARCH_USER)

sleep(15)
lis = []
dic = getFav(SEARCH_USER)

max_id = 0
count = 0

for i in dic:
    lis.append(i)

    if i["user"]["screen_name"] == USER_ID:
        count += 1
        print(i["user"]["name"])
        print(i["text"])
        print("-")

max_id = dic[-1]["id"]
        
for i in tqdm(range(c/200 + 1)):
    sleep(20)
    dic = getFavWithID(SEARCH_USER, max_id)

    if max_id == dic[-1]["id"]:
        break
    max_id = dic[-1]["id"]
    
    for j in dic[1:]:
        lis.append(j)

        if j["user"]["screen_name"] == USER_ID:
            count += 1
            print(j["user"]["name"])
            print(j["text"])
            print("-")

print(SEARCH_USER, count)


with open("../Output/out_t", "w") as f:
    for i in lis:
        f.write(i + "\n")
