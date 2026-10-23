import os
import requests
import json
from urllib.parse import parse_qs

# Google Identity Platform OIDC example
# Provider configuration – these environment variables must be set
# GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')


def exchange_code_for_tokens(code):
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json()


def handle_callback(query_params):
    # query_params is a dict from urlparse(parse_qs)
    code = query_params.get('code')
    if not code:
        raise ValueError('No authorization code in callback query parameters')
    tokens = exchange_code_for_tokens(code[0])
    # Store or return tokens as needed
    return tokens

if __name__ == '__main__':
    # Simple script to test the callback locally
    qs = parse_qs(os.environ.get('QUERY_STRING', ''))
    tokens = handle_callback(qs)
    print('Tokens received:', json.dumps(tokens, indent=2))
