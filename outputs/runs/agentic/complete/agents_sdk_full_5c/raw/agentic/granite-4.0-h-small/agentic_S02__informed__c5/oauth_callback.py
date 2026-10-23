import os
import json
import requests
from identity_client import IdentityClient

# Auth0 endpoint for token exchange (can be replaced with other providers)
TOKEN_ENDPOINT = "https://{AUTH0_DOMAIN}/oauth/token"

def exchange_code_for_tokens(authorization_code):
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

    payload = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': 'http://localhost:8000/oauth_callback',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET
    }
    # Use application/json content type for some providers
    headers = {'Content-Type': 'application/json'}
    response = requests.post(TOKEN_ENDPOINT.format(AUTH0_DOMAIN=AUTH0_DOMAIN),
                            data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    return response.json()

# Example usage
if __name__ == '__main__':
    code = input('Enter auth code: ')
    tokens = exchange_code_for_tokens(code)
    print('Tokens:', json.dumps(tokens, indent=2))

    # Pass tokens to profile_claims for retrieving user info
