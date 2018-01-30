"""Configuration"""

import os

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///database.sqlite')

TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET', '')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', '')

DOGECOIN_USER = os.getenv('DOGECOIN_NODE_USERNAME', '')
DOGECOIN_PASSWORD = os.getenv('DOGECOIN_NODE_PASSWORD', '')
DOGECOIN_HOST = os.getenv('DOGECOIN_NODE_HOST', '')
DOGECOIN_PORT = os.getenv('DOGECOIN_NODE_PORT', '')
