import os
import uuid
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from identity_client import IdentityClient
from identity_models import AuthCodeExchangeRequest, AuthCodeExchangeResponse

load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'


def oauth_callback():
    # Retrieve the authorization code from the query string (typically via a web framework)
    code = request.args.get('code')
    if not code:
        raise ValueError('Authorization code missing')
    
    exchange_req = AuthCodeExchangeRequest(
        grant_type='authorization_code',
        code=code,
        redirect_uri=REDIRECT_URI,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET
    )
    client = IdentityClient('https://{AUTH0_DOMAIN}/oauth/token')
    exchange_resp = client.exchange_code(exchange_req)
    # After a successful exchange, redirect to the next step (e.g., profile fetch)
    return redirect('/profile', code=302)

if __name__ == '__main__':
    # Simple CLI demo
    code_input = input('Enter authorization code: ')
    exchange_req = AuthCodeExchangeRequest(
        grant_type='authorization_code',
        code=code_input,
        redirect_uri=REDIRECT_URI,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET
    )
    client = IdentityClient('https://{AUTH0_DOMAIN}/oauth/token')
    exchange_resp = client.exchange_code(exchange_req)
    print('Exchange successful. Tokens received:', exchange_resp.to_dict())