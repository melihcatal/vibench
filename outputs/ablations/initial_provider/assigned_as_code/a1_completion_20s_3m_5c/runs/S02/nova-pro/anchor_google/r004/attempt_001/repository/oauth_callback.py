import requests

CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'https://yourapp.com/oauth_callback'
AUTHORIZATION_ENDPOINT = 'https://oauth.provider.com/authorize'
TOKEN_ENDPOINT = 'https://oauth.provider.com/token'
USER_INFO_ENDPOINT = 'https://oauth.provider.com/userinfo'

def get_authorization_url():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid profile email'
    }
    authorization_url = f'{AUTHORIZATION_ENDPOINT}?{urlencode(params)}'
    return authorization_url