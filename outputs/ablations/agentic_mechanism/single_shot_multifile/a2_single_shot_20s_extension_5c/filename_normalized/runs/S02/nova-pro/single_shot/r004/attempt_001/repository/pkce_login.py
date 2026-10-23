import requests
import hashlib
import base64
from identity_client import IDENTITY_CLIENT_ID, IDENTITY_REDIRECT_URI

AUTHORIZATION_ENDPOINT = 'https://oauth.reddit.com/api/v1/authorize'
TOKEN_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'

def generate_code_verifier():
    code_verifier = base64.urlsafe_b64encode(hashlib.sha256(os.urandom(30)).digest()).decode().rstrip('=')
    return code_verifier

def generate_code_challenge(code_verifier):
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip('=')
    return code_challenge

def pkce_login():
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    
    params = {
        'response_type': 'code',
        'client_id': IDENTITY_CLIENT_ID,
       'redirect_uri': IDENTITY_REDIRECT_URI,
       'scope': 'identity',
        'state': 'random_state_string',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    authorization_url = f"{AUTHORIZATION_ENDPOINT}?client_id={IDENTITY_CLIENT_ID}&response_type=code&state=random_state_string&redirect_uri={IDENTITY_REDIRECT_URI}&scope=identity&code_challenge={code_challenge}&code_challenge_method=S256"
    print(f'Redirect to: {authorization_url}')
    
    # Simulate receiving the authorization code
    code = 'your-authorization-code'
    
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
       'redirect_uri': IDENTITY_REDIRECT_URI,
        'code_verifier': code_verifier,
    }
    response = requests.post(TOKEN_ENDPOINT, data=token_data)
    tokens = response.json()
    print(tokens)

if __name__ == '__main__':
    pkce_login()