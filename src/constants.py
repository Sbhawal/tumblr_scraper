import pandas as pd

with open('credentials.txt', 'r') as f:
    keys = f.read().splitlines()
CONSUMER_KEY = keys[0].split(":")[1].strip()
CONSUMER_KEY_SECRET = keys[1].split(":")[1].strip()
TOKEN = keys[2].split(":")[1].strip()
TOKEN_SECRET = keys[3].split(":")[1].strip()
API_KEY = keys[4].split(":")[1].strip()

import pytumblr

client = pytumblr.TumblrRestClient(
  CONSUMER_KEY,
  CONSUMER_KEY_SECRET,
  TOKEN,
  TOKEN_SECRET
)


DOWNLOAD_PATH = "downloads"

limit = 50
post_dataframe = pd.DataFrame(columns=['id', 'type', 'tags', 'reblog_key', 'links'])