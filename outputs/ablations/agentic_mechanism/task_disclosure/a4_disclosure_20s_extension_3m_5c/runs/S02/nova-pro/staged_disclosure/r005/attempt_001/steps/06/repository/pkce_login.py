import requests
import json
import base64
import os
from urllib.parse import urlencode

# Auth0 configuration
AUTH0_DOMAIN = 'your-auth0-domain.auth0.com'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://localhost:3000/callback'

# PKCE code verifier and challenge
code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode('utf-8')
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8')

# Authorization URL
authorization_url = f'https://{AUTH0_DOMAIN}/authorize?{urlencode({
    'response_type': 'code',
    'client_id': CLIENT_ID,
    'redirect_uri': REDIRECT_URI,
    'code_challenge': code_challenge,
    'code_challenge_method': 'S256'
})}'

print(f'Authorization URL: {authorization_url}')

# User should visit the authorization URL and authorize the application
# After authorization, the user will be redirected to the REDIRECT_URI with a code

# Exchange authorization code for tokens
def exchange_code_for_tokens(code):
    token_url = f'https://{AUTH0_DOMAIN}/oauth/token'
    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_verifier
    }
    response = requests.post(token_url, data=token_payload)
    response.raise_for_status()
    return response.json()

# Example usage
# code = 'authorization_code_from_redirect'
# tokens = exchange_code_for_tokens(code)
# print(tokens)