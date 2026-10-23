import os

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/oauth_callback'

def get_google_client_id():
    return GOOGLE_CLIENT_ID

def get_google_client_secret():
    return GOOGLE_CLIENT_SECRET

def get_redirect_uri():
    return REDIRECT_URI