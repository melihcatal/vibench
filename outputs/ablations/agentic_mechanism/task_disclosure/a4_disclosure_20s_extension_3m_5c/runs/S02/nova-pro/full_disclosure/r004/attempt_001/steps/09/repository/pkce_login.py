import requests

OKTA_DOMAIN = 'your-okta-domain'
CLIENT_ID = 'your-client-id'
REDIRECT_URI = 'your-redirect-uri'

def generate_code_verifier():
    import base64
    import os
    import hashlib
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8')
    return code_verifier, code_challenge

def initiate_login():
    code_verifier, code_challenge = generate_code_verifier()
    auth_url = f'https://{OKTA_DOMAIN}/oauth2/v1/authorize'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid profile email',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    response = requests.get(auth_url, params=params)
    return response.url, code_verifier

def exchange_code_for_tokens(code, code_verifier):
    token_url = f'https://{OKTA_DOMAIN}/oauth2/v1/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_verifier,
        'client_id': CLIENT_ID
    }
    response = requests.post(token_url, headers=headers, data=data)
    return response.json()