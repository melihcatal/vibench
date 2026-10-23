import os
from authlib.integrations.requests_client import OAuth2Session

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

def get_oauth_client():
    return OAuth2Session(client_id=AUTH0_CLIENT_ID, redirect_uri='http://localhost:5000/callback')