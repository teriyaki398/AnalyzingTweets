import json
from requests_oauthlib import OAuth1Session
from time import sleep


with open("../.token/TwitterToken") as f:
    TOKEN = f.read().split("\n")
    TOKEN = list(map(lambda x: x.split(" "), TOKEN))[:-1]

with open("../Output/AnalyzingTweets") as f:
    USER_ID = f.read().split(" ")[1][:-1]


# request url
url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

MONTH = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", 
        "Jun":"06", "Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10",
        "Nov":"11", "Dec":"12"}

def retDateNum(dic):
    date = dic["created_at"].split(" ")
    return date[-1] + MONTH[date[1]] + date[2] + date[3].replace(":", "")


def getUsersTweets(scree_name, max_id):
    twitter = OAuth1Session(TOKEN[0][1], TOKEN[1][1], TOKEN[2][1], TOKEN[3][1])

    if max_id == -1:
        # request parameters
        params = {  "user_id": USER_ID,
                    "count": 200}
    else:
        params = {  "user_id": USER_ID,
                    "max_id": max_id,
                    "count": 200}
    
    res = twitter.get(url, params=params)
    dic = json.loads(res.text)
    return dic


lis = []

dic = getUsersTweets(USER_ID, -1)

for i in dic:
    lis.append([i["id"], retDateNum(i)])


max_id = dic[-1]["id"]
while True:
    sleep(1.1)

    print(dic[-1]["id"])
    print(len(dic))
    dic = getUsersTweets(USER_ID, max_id)

    for i in dic:
        ent = [i["id"], retDateNum(i)]

        if ent not in lis:
            lis.append(ent)
    
    if max_id == dic[-1]["id"]:
        break
    max_id = dic[-1]["id"]
    

with open("../Output/" + USER_ID + "-TWEETS", "a") as f:
    for i in lis:
        f.write(str(i[0]) + " " + i[1] + "\n")