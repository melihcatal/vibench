import os
from authlib.integrations.requests_client import OAuth2Session

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')

oauth = OAuth2Session(client_id=AUTH0_CLIENT_ID, redirect_uri='http://localhost:5000/callback', scope='openid profile email')
authorization_url, state = oauth.create_authorization_url(f'https://{AUTH0_DOMAIN}/authorize')
print('Please go to this URL and login:', authorization_url)