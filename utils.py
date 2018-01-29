"""Utils"""

def is_valid_tiptweet(tweet):
    """Checks if tweet is a valid tip tweet"""
    tweet_els = tweet.split(' ')
    return 'tip' in tweet and len(tweet_els) == 4 and '@' in tweet_els[2]
