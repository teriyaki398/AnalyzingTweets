import json
from time import sleep
from requests_oauthlib import OAuth1Session
from tqdm import tqdm

with open("../.token/TwitterToken") as f:
    TOKEN = f.read().split("\n")
    TOKEN = list(map(lambda x: x.split(" "), TOKEN))[:-1]

with open("../Output/AnalyzingTweets") as f:
    USER_ID = f.read().split(" ")[1][:-1]

with open("../Output/Followers") as f:
    followers = f.read().split("\n")[:-1]

with open("../Output/Statistics") as f:
    statis = f.read().split("\n")[:-1]

# remove searched followers
for i in statis:
    name = i.split(" ")
    if name[0] in followers:
        followers.remove(name[0])


# request url
url = "https://api.twitter.com/1.1/favorites/list.json"

def getFav(name):
    # Auth
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
    url = "https://api.twitter.com/1.1/favorites/list.json"
    params = {"screen_name": name, "max_id": id, "count": 200}
    res = twitter.get(url, params=params)
    dic = json.loads(res.text)
    return dic


def getFavoritesCount(name):
    twitter = OAuth1Session(TOKEN[0][1], TOKEN[1][1], TOKEN[2][1], TOKEN[3][1])
    url = "https://api.twitter.com/1.1/users/show.json"
    params = {"screen_name": name}
    res = twitter.get(url, params=params)
    dic = json.loads(res.text)
    return dic["favourites_count"]


for serach_user in tqdm(followers):
    fav_count = getFavoritesCount(serach_user)
    print(serach_user, fav_count)
    
    sleep(13)

    dic = getFav(serach_user)

    max_id = 0
    count = 0

    flag = True

    for i in dic:
        try:
            max_id = i["id"]

            if i["user"]["screen_name"] == USER_ID:
                count += 1
                print(i["user"]["name"])
                print(i["text"])
                print("-")
        except:
            flag = False
            
    if flag == False:
        with open("../Output/Statistics", "a") as f:
            f.write(serach_user + " 0\n")
        continue

    loopCount = fav_count / 200
    # if loopCount > 100:
    #     loopCount = 100
    for i in range(loopCount):
        sleep(13)
        dic = getFavWithID(serach_user, max_id)
        
        for j in dic[1:]:
            try:
                max_id = j["id"]

                if j["user"]["screen_name"] == USER_ID:
                    count += 1
                    print(j["user"]["name"])
                    print(j["text"])
                    print("-")
            except:
                print("exception")
        
    with open("../Output/Statistics", "a") as f:
        f.write(serach_user + " " + str(count) + "\n")

    print("Result : " + serach_user + " " + str(count) + "\n")