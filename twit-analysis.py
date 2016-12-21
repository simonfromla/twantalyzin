from collections import Counter
from local_config import *
import json
import pdb
import sys
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream

langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}


class Listener(StreamListener):
    # Add counter to code to make stream stop. Cannot add to on_data since always new call.
    # Add during init instead, so avail. each time on_data() called.
    def __init__(self, num_tweets_to_grab, retweet_count=500):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count
        self.languages = []
        self.top_languages = []

    def on_data(self, data):
        #try/except bc if find unfriendly tweet json object, skip
        try:
            json_data = json.loads(data)
            self.languages.append(langs[json_data["lang"]])

            self.counter += 1

            # Parse the json object for retweet count
            retweet_count = json_data["retweeted_status"]["retweet_count"]
            # If the count is gt what its been initialized to(8000),
            #print tweet text, count, lang, and save the top lang
            if retweet_count >= self.retweet_count:
                print(json_data["text"], retweet_count, langs[json_data["lang"]])
                self.top_languages.append(langs[json_data["lang"]])

            # These happen at function exit
            if self.counter >= self.num_tweets_to_grab:
                print(self.languages)
                print(self.top_languages)
                print(Counter(self.languages))
                print(Counter(self.top_languages))
                return False

            return True
        except:
            pass

    def on_error(self, status):
        print(status)

class TwitterMain():
    def __init__(self, num_tweets_to_grab, retweet_count):
        self.auth = tweepy.OAuthHandler(cons_tok, cons_sec)
        self.auth.set_access_token(app_tok, app_sec)
        self.api = tweepy.API(self.auth)

        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count

    def get_trends(self):
        trends = self.api.trends_place(1)
        trend_data = []

        for trend in trends[0]['trends']:
            trend_samples = []
            trend_samples.append(trend['name'])
            tweet_samples = tweepy.Cursor(self.api.search, q = trend['name'], lang = 'th').items(2)
            for tweet in tweet_samples:
                trend_samples.append(tweet.text)
            # print(tuple(trend_samples))
            trend_data.append(tuple(trend_samples))
            # print(trend_data)

        print(trend_data)



if __name__ == "__main__":
    # auth = tweepy.OAuthHandler(cons_tok, cons_sec)
    # auth.set_access_token(app_tok, app_sec)
    # twitter_api = tweepy.API(auth)

    auth = tweepy.AppAuthHandler(cons_tok, cons_sec)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    if(not api):
        print("cant authenticate")
        sys.exit(-1)


    analyze = TwitterMain(num_tweets_to_grab=50, retweet_count=5000)
    analyze.get_trends()


    # Search stuff
    # search_results = tweepy.Cursor(twitter_api.search, q = "Tim Duncan").items(5)
    # for result in search_results:
    #     print("==duncan==="+result.text)


    # # Init the counter by creating instance with specific # tweets to grab
    # twitter_stream = Stream(auth, Listener(num_tweets_to_grab=50))
    # try:
    #     twitter_stream.sample()
    # except Exception as e:
    #     print(e.__doc__)