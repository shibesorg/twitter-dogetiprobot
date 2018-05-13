# -*- coding: utf-8 -*-

"""
Go through the list of saved replies and check for accepted and tip them.
"""

import time
import pdb;
from datetime import datetime
from tweepy import RateLimitError
from db import tweets, users
from twitter_api import api
from utils import logger
from doge import dogeconn

# for status in tweepy.Cursor(api.user_timeline).items(200):
#     process_status(status)

def main():
    for tweet in tweets:
        tweet_id = tweet['tweet_id']
        reply_id = tweet['reply_id']
        search_results = []

        try:
            search_results = api.search('to:dogetiprobot', since_id=tweet_id)
        except RateLimitError:
            time.sleep(5 * 60)

        for result in search_results:
                # author_id = result.author._json['id']
                author_username = result.author._json['screen_name']

                if result.in_reply_to_status_id == reply_id and tweet['receiver_username'] == author_username and tweet['confirmed'] is False:
                    logger.info('Tx is not completed, proceeding to tip')

                    text = result.text

                    parent_tweet = api.get_status(tweet_id)

                    logger.info('Parent tweet %s', parent_tweet.text)
                    logger.info('Reply: %s', text)

                    if 'accept' in text:
                        logger.info('%s has accepted the tip', tweet['receiver_username'])

                        user = users.find_one(user_id=tweet['receiver_id'])

                        # If user does not have a dogecoin address create one.
                        if not user:
                            logger.info('%s has not wallet, creating one', tweet['receiver_username'])

                            user_id = tweet['receiver_id']
                            address = dogeconn.get_newaddress(str(user_id))
                            users.insert(dict(
                                user_id=tweet['receiver_id'],
                                address=address,
                                created_at=datetime.utcnow(),
                            ))                    

                            # send dogecoins
                            logger.info('Sending a Ð%s tip from %s to %s at this address %s', tweet['amount'], tweet['sender_username'], tweet['receiver_username'], address)

                            tx = dogeconn.send_from(
                                str(tweet['sender_id']),
                                address,
                                float(tweet['amount']),
                                comment='@{0} sent you Ð{1} from Twitter through @dogetiprobot'.format(
                                    tweet['sender_id'],
                                    tweet['amount'],
                                )
                            )
                            tweets.update(dict(
                                tweet_id=tweet_id,
                                completed=True,
                                accepted=True,
                                modified_at=datetime.utcnow(),
                                tx=tx,
                            ), ['tweet_id'])
                        else:
                            # send dogecoins
                            logger.info('Sending a %s tip from %s to %s at this address %s', tweet['amount'], tweet['sender_username'], tweet['receiver_username'], user['address'])

                            tx = dogeconn.send_from(
                                str(tweet['sender_id']),
                                user['address'],
                                float(tweet['amount']),
                                comment='@{0} sent you Ð{1} from Twitter through @dogetiprobot'.format(
                                    tweet['sender_id'],
                                    tweet['amount'],
                                )
                            )
                            tweets.update(dict(
                                tweet_id=tweet_id,
                                completed=True,
                                accepted=True,
                                modified_at=datetime.utcnow(),
                                tx=tx,
                            ), ['tweet_id'])
                    if 'decline' in text:
                        logger.warn('Receiver declined tip. Complete transaction.')
                        tweets.update(dict(
                            tweet_id=tweet_id,
                            completed=True,
                            accepted=False,
                            confirmed=True,
                            modified_at=datetime.utcnow(),
                        ), ['tweet_id'])


if __name__ == '__main__':
    main()
