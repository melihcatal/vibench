import os

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
USERINFO_URL = 'https://openidconnect.googleapis.com/v1/userinfo'

def get_client_id():
    return CLIENT_ID

def get_client_secret():
    return CLIENT_SECRET

def get_auth_url():
    return AUTH_URL

def get_token_url():
    return TOKEN_URL

def get_userinfo_url():
    return USERINFO_URL