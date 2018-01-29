import tweepy
from config import (TWITTER_ACCESS_TOKEN, TWITTER_CONSUMER_KEY,
                    TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN_SECRET)


auth = tweepy.OAuthHandler(
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)

auth.set_access_token(
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
)

api = tweepy.API(auth)
