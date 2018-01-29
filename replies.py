# -*- coding: utf-8 -*-

"""
Check in frontier for unreplied tweets and ask the receiver if they accept the tip.
If they do, we add the tip to a queue that `tip.py` will execute later.
"""

import time
from db import tweets
from twitter_api import api
from doge import dogeconn

def main():
    for tweet in tweets.all():
        if tweet['replied'] is False:
            balance = dogeconn.get_balance(tweet['sender_id'])
            if (balance < tweet['amount']):
                # reply with not enough balance and give an address to deposit
                print('not enough doge to send')
            else:
                status = api.update_status('@{0}, @{1} sent you a Ð{2} tip, reply with accept to accept the tip or decline to decline it.'.format(tweet['receiver_username'], tweet['sender_username'], tweet['amount']))
                try:
                    tweets.update(dict(
                        tweet_id=tweet['tweet_id'],
                        replied=True,
                        reply_id=status.id,
                    ), ['tweet_id'])
                except Exception as e:
                    print('error')
                    print(e)

                print(tweet)
                time.sleep(3)


if __name__ == '__main__':
    main()