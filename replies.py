# -*- coding: utf-8 -*-

"""
Check in frontier for unreplied tweets and ask the receiver if they accept the tip.
If they do, we add the tip to a queue that `tip.py` will execute later.
"""

import time
from datetime import datetime
from tweepy import TweepError
from db import tweets
from utils import logger
from twitter_api import api
from doge import dogeconn

def main():
    for tweet in tweets.all():
        if tweet['replied'] is False:
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
                    status = api.update_status(reply_msg)
                    tweets.update(dict(
                        tweet_id=tweet['tweet_id'],
                        replied=True,
                        reply_id=status.id,
                        completed=True,
                        accepted=False,
                        modified_at=datetime.utcnow(),
                    ), ['tweet_id'])
                except TweepError as e:
                    error_code = e.message[0]['code']
                    if error_code == 187:
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
                    status = api.update_status('@{0}, @{1} sent you a Ð{2} tip, reply with accept to accept the tip or decline to decline it.'.format(tweet['receiver_username'], tweet['sender_username'], tweet['amount']))

                    tweets.update(dict(
                        tweet_id=tweet['tweet_id'],
                        replied=True,
                        reply_id=status.id,
                        completed=True,
                        accepted=False,
                        modified_at=datetime.utcnow(),
                    ), ['tweet_id'])
                except TweepError as e:
                    logger.info('User already send this tip resulting in duplicated tweet. Recomending him to try a different amount')
                    error_code = e.message[0]['code']
                    if error_code == 187:
                        logger.info('Duplicated tweet, we are passing on it.')
                            
                        status = api.update_status('@{1} it seems you already tried to send this amount to the same user, please try a different amount because Twitter does not allow duplicated tweets, thanks.'.format(tweet['receiver_username'], tweet['sender_username'], tweet['amount']))

                        tweets.update(dict(
                            tweet_id=tweet['tweet_id'],
                            replied=True,
                            reply_id=status.id,
                            completed=True,
                            accepted=False,
                            modified_at=datetime.utcnow(),
                        ), ['tweet_id'])
                    else:
                        logger.error(e)


                logger.info('Waiting 3 seconds...')
                time.sleep(3)


if __name__ == '__main__':
    main()