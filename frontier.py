# -*- coding: utf-8 -*-

"""
It looks for mentions and save the ones containing a valid tip sentence,
that's it: 'tip @user amount'.
"""

from datetime import datetime
import tweepy
from db import tweets
from utils import is_valid_tiptweet, logger
from twitter_api import api

def main():
    """Main function"""

    # TODO: Check if user has account and save tweet if it does if not
    # there is no case
    for mention in tweepy.Cursor(api.mentions_timeline).items():
        user_id = mention.user.id
        username = mention.user.screen_name
        tweet_id = mention.id
        tweet = mention.text
        tweet_els = tweet.split(' ')

        logger.info('Reading %s', tweet)

        # Searches for the tweet in the database
        tweet_ = tweets.find_one(tweet_id=tweet_id)

        # If it's a valid tweet and hasn't been saved before
        if is_valid_tiptweet(tweet) and not tweet_:
            receiver_id = mention.entities['user_mentions'][1]['id']
            receiver_username = mention.entities['user_mentions'][1]['screen_name']

            amount = tweet_els[3]

            logger.info('Saving tweet')

            tweets.insert(dict(
                tweet_id=tweet_id,
                completed=False,
                accepted=False,
                replied=False,
                reply_id=0,
                sender_id=user_id,
                sender_username=username,
                receiver_id=receiver_id,
                receiver_username=receiver_username,
                amount=amount,
                created_at=datetime.utcnow(),
                modified_at=datetime.utcnow(),
                tx='',
                confirmed=False,
            ))


if __name__ == '__main__':
    main()
