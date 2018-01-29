"""Database"""

import dataset
from config import DATABASE_URI

# Database
database = dataset.connect(DATABASE_URI)
users = database['users']
tweets = database['tweets']
