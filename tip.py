# -*- coding: utf-8 -*-

"""
Go through the list of saved replies and check for accepted and tip them.
"""

from datetime import datetime
from db import tweets, users
from twitter_api import api
from doge import dogeconn

# for status in tweepy.Cursor(api.user_timeline).items(200):
#     process_status(status)

def main():
    for tweet in tweets:
        tweet_id = tweet['tweet_id']
        reply_id = tweet['reply_id']
        print('tweet id: {0}'.format(tweet_id))
        print('reply id: {0}'.format(reply_id))
        print('sender: {0}'.format(tweet['sender_username']))
        print('receiver: {0}'.format(tweet['receiver_username']))

        search_results = api.search('to:dogetiprobot', since_id=tweet_id)

        for result in search_results:
                author_id = result.author._json['id']
                author_username = result.author._json['screen_name']

                if result.in_reply_to_status_id == reply_id and tweet['receiver_username'] == author_username:
                    text = result.text

                    if 'accept' in text:
                        # Check if sender has enough balance
                        # if not ignore
                        print('send tip!')
                        print('is reply!')
                        print('text: {0}'.format(text))
                        print('reply id: {0}'.format(result.in_reply_to_status_id))

                        user = users.find_one(user_id=tweet['receiver_id'])

                        if not user:
                            user_id = tweet['receiver_id']
                            address = dogeconn.get_newaddress(user_id)
                            users.insert(dict(
                                user_id=tweet['receiver_id'],
                                address=address,
                                created_at=datetime.utcnow(),
                            ))                    
                            # send dogecoins
                        else:
                            #  send dogecoins
                            print('yo')

                        print('author id: {0}'.format(author_id))
                        print('author username: {0}'.format(author_username))
                        print('Author is receiver: {0}'.format(tweet['receiver_username'] == author_username))
                    if 'decline' in text:
                        tweets.update(dict(
                            tweet_id=tweet_id,
                            completed=True,
                            accepted=False,
                            modified_at=datetime.utcnow(),
                        ), ['tweet_id'])

if __name__ == '__main__':
    main()