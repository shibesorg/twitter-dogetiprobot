"""Utils"""

import logging
import coloredlogs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

coloredlogs.install(level='DEBUG', logger=logger)

handler = logging.FileHandler('dogetiprobot.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
handler.setFormatter(formatter)

# logger.debug("this is a debugging message")
# logger.info("this is an informational message")
# logger.warning("this is a warning message")
# logger.error("this is an error message")
# logger.critical("this is a critical message")


def is_valid_tiptweet(tweet):
    """Checks if tweet is a valid tip tweet"""
    tweet_els = tweet.split(' ')
    return 'tip' in tweet and len(tweet_els) == 4 and '@' in tweet_els[2]
