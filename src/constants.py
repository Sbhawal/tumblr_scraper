import pickle

with open('keys.pkl', 'rb') as f:
    keys = pickle.load(f)
    
CONSUMER_KEY = keys[0]
CONSUMER_KEY_SECRET = keys[1]
TOKEN = keys[2]
TOKEN_SECRET = keys[3]
API_KEY = keys[4]

