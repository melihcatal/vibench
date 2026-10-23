import os
import requests
from identity_client import IdentityClient
from identity_models import OAuthCallbackResponse

def oauth_callback(code, state):
    client = IdentityClient.from_env()
    # Use Auth0 for token exchange
    AUTH0_DOMAIN = client.config['AUTH0_DOMAIN']
    CLIENT_ID = client.config['CLIENT_ID']
    CLIENT_SECRET = client.config['CLIENT_SECRET']
    token_url = f'https://{AUTH0_DOMAIN}/oauth/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': client.config['REDIRECT_URI'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    data = response.json()
    # Exchange successful, return normalized tokens
    return OAuthCallbackResponse(**data)

if __name__ == '__main__':
    # Example usage with mock code and state
    tokens = oauth_callback('mock_code', 'mock_state')
    print('Access token:', tokens.access_token)
