import os
from authlib.integrations.requests_client import OAuth2Session
from authlib.jose import rfc7517, rfc7519
import hashlib
import base64

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')

code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode('utf-8')
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8')

oauth = OAuth2Session(client_id=AUTH0_CLIENT_ID, redirect_uri='http://localhost:5000/callback', scope='openid profile email')
authorization_url, state = oauth.create_authorization_url(f'https://{AUTH0_DOMAIN}/authorize', code_challenge=code_challenge, code_challenge_method='S256')
print('Please go to this URL and login:', authorization_url)