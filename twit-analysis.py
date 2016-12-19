import json
from local_config import *
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream


class listener(StreamListener):
    def on_data(self, data):
        j = json.loads(data)
        print(j["text"])
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    auth = tweepy.OAuthHandler(cons_tok, cons_sec)
    auth.set_access_token(app_tok, app_sec)
    twitter_api = tweepy.API(auth)

    # Search stuff
    search_results = tweepy.Cursor(twitter_api.search, q = "Tim Duncan").items(5)
    for result in search_results:
        print(result.text)

    trends = twitter_api.trends_place(1)

    for trend in trends[0]["trends"]:
        print(trend['name'])