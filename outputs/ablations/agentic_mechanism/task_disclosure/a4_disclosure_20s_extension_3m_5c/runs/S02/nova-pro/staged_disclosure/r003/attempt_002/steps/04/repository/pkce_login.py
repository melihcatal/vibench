import requests
import base64
import json

# Auth0 configuration
AUTH0_DOMAIN = 'your-auth0-domain'
CLIENT_ID = 'your-client-id'
REDIRECT_URI = 'your-redirect-uri'

# Generate a code verifier
def generate_code_verifier():
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode('utf-8').replace('=', '')
    return code_verifier

# Generate a code challenge from the code verifier
def generate_code_challenge(code_verifier):
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode('utf-8').replace('=', '')
    return code_challenge

# Obtain authorization code
def get_authorization_code(code_challenge):
    auth_url = f'https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&code_challenge={code_challenge}&code_challenge_method=S256'
    print(f'Please visit this URL to authorize: {auth_url}')
    code = input('Enter the authorization code from the redirect URL: ')
    return code

# Exchange authorization code for tokens
def exchange_code_for_tokens(code, code_verifier):
    token_url = f'https://{AUTH0_DOMAIN}/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'code_verifier': code_verifier,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    tokens = response.json()
    return tokens

# Main PKCE login flow
def pkce_login():
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    code = get_authorization_code(code_challenge)
    tokens = exchange_code_for_tokens(code, code_verifier)
    print('Access Token:', tokens['access_token'])
    print('ID Token:', tokens['id_token'])
    print('Refresh Token:', tokens['refresh_token'])

if __name__ == '__main__':
    pkce_login()