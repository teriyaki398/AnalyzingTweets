import json
from requests_oauthlib import OAuth1Session


with open("../.token/TwitterToken") as f:
    TOKEN = f.read().split("\n")
    TOKEN = list(map(lambda x: x.split(" "), TOKEN))[:-1]

with open("../.user_settings/AnalyzingTweets") as f:
    USER_ID = f.read().split(" ")[1][:-1]

for i in TOKEN:
    print(i)

print(USER_ID)

twitter = OAuth1Session(TOKEN[0][1], TOKEN[1][1], TOKEN[2][1], TOKEN[3][1])

# request url
url = "https://api.twitter.com/1.1/favorites/list.json"

# request parameters
params = {"user_id": USER_ID}

# rewuest
res = twitter.get(url, params=params)

# json -> dict
fav_dic = json.loads(res.text)

for i in fav_dic:
    print(i[u'text'])
