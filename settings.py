TRACK_TERMS = ["NBA", "basketball", "lebron", "curry", "warriors", "cavs"]
TRACK_USER_ID = [""]
NUM_TWEETS_TO_GRAB = 100
CONNECTION_STRING = ""
CSV_NAME = "twantalyzin.csv"
TABLE_NAME = "Stream_Results"

try:
    from local_config import *
except Exception:
    pass