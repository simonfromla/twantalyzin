import json
from local_config import *
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream


class listener(StreamListener):
    # Add counter to code to make stream stop. Cannot add to on_data since always new call.
    # Add during init instead, so avail. each time on_data() called.
    def __init__(self, num_tweets_to_grab):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab

    def on_data(self, data):
        #try/except bc if find unfriendly tweet json object, skip
        try:
            j = json.loads(data)
            print(j["text"])
            return True
        except:
            pass

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

    twitter_stream = Stream(auth, twitter_listener(num_tweets_to_grab=5))
    try:
        twitter_stream.sample()
    except Exception as e:
        print(e.__doc__)