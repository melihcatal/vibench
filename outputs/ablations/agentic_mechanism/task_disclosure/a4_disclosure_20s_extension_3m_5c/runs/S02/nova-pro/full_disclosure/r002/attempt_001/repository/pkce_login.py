import requests
import base64
import hashlib
import uuid

# Google OAuth 2.0 configuration
GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'
GOOGLE_CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'
GOOGLE_AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'
GOOGLE_REDIRECT_URI = 'http://localhost:8000/oauth2callback'


def generate_code_verifier():
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode('utf-8').replace('=', '')
    return code_verifier


def generate_code_challenge(code_verifier):
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').replace('=', '')
    return code_challenge


def get_authorization_url(code_challenge):
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
    }
    authorization_url = f"{GOOGLE_AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}"
    return authorization_url


def exchange_code_for_tokens(code, code_verifier):
    data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code_verifier': code_verifier,
    }
    response = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    authorization_url = get_authorization_url(code_challenge)
    print(f'Please visit this URL to authorize the application: {authorization_url}')
    # After authorization, the user will be redirected to the redirect_uri with a code
    # You need to capture the code from the redirect_uri and use it to exchange for tokens
    # code = 'CAPTURED_AUTHORIZATION_CODE'
    # tokens = exchange_code_for_tokens(code, code_verifier)
    # print(tokens)