import json
from requests_oauthlib import OAuth1Session


with open("../.token/TwitterToken") as f:
    TOKEN = f.read().split("\n")
    TOKEN = list(map(lambda x: x.split(" "), TOKEN))[:-1]

with open("../.AnalyzingTweets/AnalyzingTweets") as f:
    USER_ID = f.read().split(" ")[1][:-1]

for i in TOKEN:
    print(i)

print(USER_ID)

twitter = OAuth1Session(TOKEN[0][1], TOKEN[1][1], TOKEN[2][1], TOKEN[3][1])

# request url
url = "https://api.twitter.com/1.1/followers/list.json"

# request parameters
params = {  "user_id": USER_ID,
            "count": 200}

# rewuest
res = twitter.get(url, params=params)

# json -> dict
dic = json.loads(res.text)

print(len(dic["users"]), "users")

for i in dic["users"]:
    print("-")
    print(i["name"])
    print("@" + i["screen_name"])


with open("../.AnalyzingTweets/Followers", "w") as f:
    for i in dic["users"]:
        f.write(i["screen_name"] + "\n")
