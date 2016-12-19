import json
from local_config import *
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream

langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}


class listener(StreamListener):
    # Add counter to code to make stream stop. Cannot add to on_data since always new call.
    # Add during init instead, so avail. each time on_data() called.
    def __init__(self, num_tweets_to_grab, retweet_count=8000):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab
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

    # Init the counter by creating instance with specific # tweets to grab
    twitter_stream = Stream(auth, twitter_listener(num_tweets_to_grab=5))
    try:
        twitter_stream.sample()
    except Exception as e:
        print(e.__doc__)