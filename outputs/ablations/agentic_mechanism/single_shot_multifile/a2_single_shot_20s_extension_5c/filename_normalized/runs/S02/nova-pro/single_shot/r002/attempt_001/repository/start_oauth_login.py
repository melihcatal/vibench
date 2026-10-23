import os
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def start_oauth_login(app):
    google = oauth.register(
        name='google',
        client_id=os.environ['GOOGLE_CLIENT_ID'],
        client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
        authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
        authorize_params=None,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        refresh_token_url=None,
        redirect_uri='http://127.0.0.1:5000/oauth_callback',
        client_kwargs={'scope': 'openid email profile'},
    )
    return google.authorize_redirect(app, 'openid email profile')