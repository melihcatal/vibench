import os
from authlib.integrations.flask_client import OAuth
import secrets

oauth = OAuth()

def pkce_login(app):
    code_verifier = secrets.token_urlsafe(96)
    code_challenge = secrets.token_hex(32)
    google = oauth.register(
        name='google',
        client_id=os.environ['GOOGLE_CLIENT_ID'],
        authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
        authorize_params={'code_challenge': code_challenge, 'code_challenge_method': 'S256'},
        access_token_url='https://accounts.google.com/o/oauth2/token',
        redirect_uri='http://127.0.0.1:5000/oauth_callback',
        client_kwargs={'scope': 'openid email profile'},
    )
    return google.authorize_redirect(app, 'openid email profile'), code_verifier