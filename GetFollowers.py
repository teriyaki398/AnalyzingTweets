import json
from requests_oauthlib import OAuth1Session
from time import sleep


with open("../.token/TwitterToken") as f:
    TOKEN = f.read().split("\n")
    TOKEN = list(map(lambda x: x.split(" "), TOKEN))[:-1]

with open("../Output/AnalyzingTweets") as f:
    USER_ID = f.read().split(" ")[1][:-1]

for i in TOKEN:
    print(i)

print(USER_ID)


def WriteAns(ent):
    with open("../Output/"+USER_ID+"-Followers", "a") as f:
        f.write(ent["screen_name"] + "\n")


def GetFollowres(next):

    twitter = OAuth1Session(TOKEN[0][1], TOKEN[1][1], TOKEN[2][1], TOKEN[3][1])

    # request url
    url = "https://api.twitter.com/1.1/followers/list.json"

    if next == 0:
        # request parameters
        params = {  "screen_name": USER_ID,
                    "count": 200,
                }
    else:
        params = {"screen_name": USER_ID,
                    "count":200,
                    "cursor": next}

    # rewuest
    res = twitter.get(url, params=params)

    # json -> dict
    dic = json.loads(res.text)

    return dic

dic = GetFollowres(0)

ans = []

while len(ans) < 410:
    sleep(65)
    print(len(dic["users"]), "users")

    for i in dic["users"]:
        print("-")
        print(i["name"])
        print("@" + i["screen_name"])

    for i in dic["users"]:
        if i["screen_name"] not in ans:
            print(i["screen_name"])
            print("-")
            WriteAns(i)
            ans.append(i["screen_name"])

    if dic["next_cursor"] == 0:
        break

    dic = GetFollowres(dic["next_cursor"])
