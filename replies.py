# -*- coding: utf-8 -*-

"""
Check in frontier for unreplied tweets and ask the receiver if they accept the tip.
If they do, we add the tip to a queue that `tip.py` will execute later.
"""

import time
import pdb;
from datetime import datetime
from tweepy import TweepError, RateLimitError
from db import tweets
from utils import logger
from twitter_api import api
from doge import dogeconn

def main():
    for tweet in tweets.all():
        if tweet['replied'] is True and tweet['completed'] is True and tweet['accepted'] is True and tweet['confirmed'] is False:
            # pdb.set_trace()
            logger.info('User has accepted the tip and transaction was successful, we are sending confirmation tweet')

            confirmation_msg = '@{0} you have received Ð{1} from @{2}! tx: {3}'.format(
                tweet['receiver_username'],
                tweet['amount'],
                tweet['sender_username'],
                tweet['tx'],
            )

            try:
                # pdb.set_trace()
                status = api.update_status(
                    confirmation_msg,
                )

                tweets.update(dict(
                    tweet_id=tweet['tweet_id'],
                    confirmed=True,
                ), ['tweet_id'])
                logger.info('Confirmation tweet sent and database updated')
            except RateLimitError:
                logger.warn('Rate limit error, sleeping for a while.')
                time.sleep(15 * 60)

        if tweet['replied'] is False:
            logger.info('Tweet has not been replied, trying to tip user @%s', tweet['receiver_username'])

            balance = dogeconn.get_balance(str(tweet['sender_id']))

            logger.info('%s balance is %s, amount to send %s ', tweet['sender_username'], balance, tweet['amount'])

            # Make sure we have enough doges! 
            if (balance < float(tweet['amount'])):
                
                logger.info('%s has insufficient funds, ignoring and completing transaction.', tweet['sender_username'])

                reply_msg = '@{0} your tip for Ð{1} to {2} could not be completed, insufficient funds.'.format(
                    tweet['sender_username'],
                    tweet['amount'],
                    tweet['receiver_username'],
                )

                logger.info('Trying to tweet: "%s" and update database.', reply_msg)

                try:
                    # pdb.set_trace()
                    status = api.update_status(reply_msg)
                    tweets.update(dict(
                        tweet_id=tweet['tweet_id'],
                        replied=True,
                        reply_id=status.id,
                        completed=True,
                        accepted=False,
                        modified_at=datetime.utcnow(),
                    ), ['tweet_id'])
                except RateLimitError:
                    logger.warn('Rate limit hit, sleeping for a while.')
                    time.sleep(15 * 60)
                except TweepError as e:
                    error_code = e.message[0]['code']
                    if error_code == 187:
                        # pdb.set_trace()
                        logger.info('Duplicated tweet, we are passing on it.')
                        tweets.update(dict(
                            tweet_id=tweet['tweet_id'],
                            replied=True,
                            reply_id=0,
                            completed=True,
                            accepted=False,
                            modified_at=datetime.utcnow(),
                        ), ['tweet_id'])
                    else:
                        logger.error(e)
                logger.info('Waiting 3 seconds...')
                time.sleep(3)
            else:
                logger.info('%s has sufficient funds, proceeding with the transaction.', tweet['sender_username'])
                try:

                    # pdb.set_trace()
                    status = api.update_status('@{0}, @{1} sent you a Ð{2} tip, reply with accept to accept the tip or decline to decline it.'.format(tweet['receiver_username'], tweet['sender_username'], tweet['amount']))

                    tweets.update(dict(
                        tweet_id=tweet['tweet_id'],
                        replied=True,
                        reply_id=status.id,
                        completed=True,
                        accepted=False,
                        modified_at=datetime.utcnow(),
                        confirmed=False,
                    ), ['tweet_id'])
                except RateLimitError:
                    logger.warn('Rate limit hitted, sleeping for a while.')
                    time.sleep(15 * 60)
                except TweepError as e:
                    logger.warn('User already send this tip resulting in duplicated tweet. Recomending him to try a different amount')
                    error_code = e.message[0]['code']
                    if error_code == 187:
                        # pdb.set_trace()
                        logger.info('Duplicated tweet, we are passing on it.')
                            
                        status = api.update_status('@{0} it seems you already tried to send this amount to the same user, please try a different amount because Twitter does not allow duplicated tweets, thanks.'.format(tweet['sender_username']))

                        tweets.update(dict(
                            tweet_id=tweet['tweet_id'],
                            replied=True,
                            reply_id=status.id,
                            completed=True,
                            accepted=False,
                            modified_at=datetime.utcnow(),
                            confirmed=True,
                        ), ['tweet_id'])
                    else:
                        logger.error(e)
                logger.info('Waiting 3 seconds...')
                time.sleep(3)


if __name__ == '__main__':
    main()