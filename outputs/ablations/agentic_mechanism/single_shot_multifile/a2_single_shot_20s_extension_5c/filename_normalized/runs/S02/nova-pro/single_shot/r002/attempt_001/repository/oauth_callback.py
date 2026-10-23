import os
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def oauth_callback(app):
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
    user_info = resp.json()
    return user_info