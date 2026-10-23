import requests
import base64
import uuid
import json

# Auth0 configuration
AUTH0_DOMAIN = 'your-auth0-domain'
CLIENT_ID = 'your-client-id'
REDIRECT_URI = 'your-redirect-uri'

# Step 1: Generate a code verifier and code challenge
code_verifier = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8')
code_challenge = base64.urlsafe_b64encode(
    base64.urlsafe_b64decode(code_verifier)
).decode('utf-8')

# Step 2: Redirect the user to the Auth0 authorization endpoint
authorization_endpoint = f'https://{AUTH0_DOMAIN}/authorize'
authorization_params = {
    'response_type': 'code',
    'client_id': CLIENT_ID,
    'redirect_uri': REDIRECT_URI,
    'code_challenge': code_challenge,
    'code_challenge_method': 'S256',
}

# Step 3: Handle the redirect and exchange the authorization code for tokens
def exchange_code_for_tokens(authorization_code):
    token_endpoint = f'https://{AUTH0_DOMAIN}/oauth/token'
    token_params = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_verifier,
    }
    response = requests.post(token_endpoint, data=token_params)
    response.raise_for_status()
    return response.json()

# Example usage
# authorization_code = 'your-authorization-code'
# tokens = exchange_code_for_tokens(authorization_code)
# print(tokens)