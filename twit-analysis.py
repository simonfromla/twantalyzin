from collections import Counter
import dataset
from local_config import *
import json
import pdb
import settings
import sys
from textblob import TextBlob
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
    def __init__(self, num_tweets_to_grab):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab
        self.languages = []


    def on_data(self, data):
        #try/except bc if find unfriendly tweet json object, skip
        try:
            json_data = json.loads(data)

            # retweets = json_data["retweeted_status"]["retweet_count"]
            # print(json_data["retweeted_status"]["retweet_count"])
            if not json_data['retweeted'] and 'RT @' not in json_data['text']:
                # print(json_data["text"])


                description = json_data["user"]["description"]
                loc = json_data["user"]["location"]
                text = json_data["text"]

                coords = json_data["coordinates"]
                name = json_data["user"]["screen_name"]
                user_created = json_data["user"]["created_at"]
                followers = json_data["user"]["followers_count"]
                id_str = json_data["id_str"]
                created = json_data["created_at"]
                # retweets = json_data["retweeted_status"]["retweet_count"]
                # print(json_data["retweeted_status"])
                bg_color = json_data["user"]["profile_background_color"]
                blob = TextBlob(text)
                sentiment = blob.sentiment
                polarity = sentiment.polarity
                subjectivity = sentiment.subjectivity
                # print(sentiment.polarity)

                if coords is not None:
                    coords = json.dumps(coords)


                self.languages.append(langs[json_data["lang"]])

                self.counter += 1

            # Parse the json object for retweet count
            # retweet_count = json_data["retweeted_status"]["retweet_count"]
            # retweet_count = json_data["retweet_count"]


            # If the count is gt what its been initialized to(8000),
            #print tweet text, count, lang, and save the top lang
                print(json_data["text"], langs[json_data["lang"]])


                # These happen at function exit
                if self.counter >= self.num_tweets_to_grab:
                    print(self.languages)
                    print(Counter(self.languages))
                    return False

                # return True

                table = db[settings.TABLE_NAME]

                try:
                    table.insert(dict(
                    user_description=description,
                    user_location=loc,
                    coordinates=coords,
                    text=text,
                    user_name=name,
                    user_created=user_created,
                    user_followers=followers,
                    id_str=id_str,
                    created=created,
                    user_bg_color=bg_color,
                    polarity=polarity,
                    subjectivity=subjectivity,
                ))
                except ProgrammingError as err:
                    print(err)

                return True

        except:
            pass

    def on_error(self, status):
        print(status)

class TwitterMain():
    def __init__(self, num_tweets_to_grab):
            # access token auth
        self.auth = tweepy.OAuthHandler(cons_tok, cons_sec)
        self.auth.set_access_token(app_tok, app_sec)
        self.api = tweepy.API(self.auth)

            #Cannot grab streaming data with App Only Auth
        # self.auth = tweepy.AppAuthHandler(cons_tok, cons_sec)
        # self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        # if(not self.api):
        #     print("cant authenticate")
        #     sys.exit(-1)

        self.num_tweets_to_grab = num_tweets_to_grab

    def get_trends(self):
        trends = self.api.trends_place(23424960)
        trend_data = []

        for trend in trends[0]['trends']:
            trend_samples = []
            trend_samples.append(trend['name'])
            tweet_samples = tweepy.Cursor(self.api.search, q = trend['name'], lang = 'en').items(1)
            for tweet in tweet_samples:
                trend_samples.append(tweet.text)
                # print(tweet.text)
            trend_data.append(tuple(trend_samples))
            # print(trend_data)

        print(trend_data)

    def get_data_stream(self):
        # Init the counter by creating instance with specific # tweets to grab
        data_stream = Stream(self.auth, Listener(num_tweets_to_grab=self.num_tweets_to_grab))
        try:
            # data_stream.filter(follow=["BBCBreaking"])
            data_stream.filter(track=settings.TRACK_TERMS or None, follow=settings.TRACK_USER_ID or None)
            # data_stream.sample()
        except Exception as e:
            print(e.__doc__)

if __name__ == "__main__":
        # access token auth
    # auth = tweepy.OAuthHandler(cons_tok, cons_sec)
    # auth.set_access_token(app_tok, app_sec)
    # twitter_api = tweepy.API(auth)
        #app only auth
    # auth = tweepy.AppAuthHandler(cons_tok, cons_sec)
    # api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # if(not api):
    #     print("cant authenticate")
    #     sys.exit(-1)
    num_tweets_to_grab = settings.NUM_TWEETS_TO_GRAB
    # retweet_count = 500
    db = dataset.connect(settings.CONNECTION_STRING)
    analyze = TwitterMain(num_tweets_to_grab)
    # analyze.get_trends()
    analyze.get_data_stream()