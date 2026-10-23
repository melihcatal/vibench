import requests
import base64
import hashlib
import uuid

# Auth0 configuration
AUTH0_DOMAIN = 'your-auth0-domain.auth0.com'
CLIENT_ID = 'your-client-id'
REDIRECT_URI = 'your-redirect-uri'

# Step 1: Generate a code verifier and code challenge
code_verifier = base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('utf-8')
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')

# Step 2: Redirect the user to the Auth0 authorization endpoint
authorization_endpoint = f'https://{AUTH0_DOMAIN}/authorize'
authorization_params = {
    'response_type': 'code',
    'client_id': CLIENT_ID,
    'redirect_uri': REDIRECT_URI,
    'code_challenge': code_challenge,
    'code_challenge_method': 'S256',
    'scope': 'openid profile email'
}

print(f'Redirect the user to: {authorization_endpoint}?{urllib.parse.urlencode(authorization_params)}')

# Step 3: Handle the redirect and exchange the authorization code for tokens
def exchange_code_for_tokens(authorization_code):
    token_endpoint = f'https://{AUTH0_DOMAIN}/oauth/token'
    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code_verifier': code_verifier,
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_endpoint, data=token_payload)
    response.raise_for_status()
    return response.json()

# Example usage:
# authorization_code = 'your-authorization-code'
# tokens = exchange_code_for_tokens(authorization_code)
# print(tokens)