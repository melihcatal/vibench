import os

IDENTITY_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
IDENTITY_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
IDENTITY_REDIRECT_URI = os.getenv('REDDIT_REDIRECT_URI')

def get_client_id():
    return IDENTITY_CLIENT_ID

def get_client_secret():
    return IDENTITY_CLIENT_SECRET

def get_redirect_uri():
    return IDENTITY_REDIRECT_URI