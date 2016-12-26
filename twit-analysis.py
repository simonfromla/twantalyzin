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

# For lang analysis, checkout sentAnalysis branch
# langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
#          'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
#          'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
#          'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
#          'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}




class Listener(StreamListener):
    def __init__(self, num_tweets_to_grab):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab

    def on_data(self, data):
    # Load JSON, connect to DB and insert data
        try:
            json_data = json.loads(data)

            if not json_data['retweeted'] and 'RT @' not in json_data['text']:
                description = json_data["user"]["description"]
                loc = json_data["user"]["location"]
                text = json_data["text"]
                coords = json_data["coordinates"]
                name = json_data["user"]["screen_name"]
                user_created = json_data["user"]["created_at"]
                followers = json_data["user"]["followers_count"]
                id_str = json_data["id_str"]
                created = json_data["created_at"]
                bg_color = json_data["user"]["profile_background_color"]
                blob = TextBlob(text)
                sentiment = blob.sentiment
                polarity = sentiment.polarity
                subjectivity = sentiment.subjectivity

                if coords is not None:
                    coords = json.dumps(coords)

                self.counter += 1
                if self.counter >= self.num_tweets_to_grab:
                    return False

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

        self.num_tweets_to_grab = num_tweets_to_grab

    def get_data_stream(self):
        data_stream = Stream(self.auth, Listener(num_tweets_to_grab=self.num_tweets_to_grab))
        try:
            data_stream.filter(track=settings.TRACK_TERMS or None, follow=settings.TRACK_USER_ID or None)
        except Exception as e:
            print(e.__doc__)

if __name__ == "__main__":
        #app only auth
    # auth = tweepy.AppAuthHandler(cons_tok, cons_sec)
    # api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # if(not api):
    #     print("cant authenticate")
    #     sys.exit(-1)
    num_tweets_to_grab = settings.NUM_TWEETS_TO_GRAB
    db = dataset.connect(settings.CONNECTION_STRING)
    analyze = TwitterMain(num_tweets_to_grab)
    analyze.get_data_stream()