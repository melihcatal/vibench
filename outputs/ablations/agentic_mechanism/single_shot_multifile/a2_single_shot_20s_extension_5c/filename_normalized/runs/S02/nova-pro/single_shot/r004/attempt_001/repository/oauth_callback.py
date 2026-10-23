import requests
from identity_client import IDENTITY_CLIENT_ID, IDENTITY_CLIENT_SECRET, IDENTITY_REDIRECT_URI

TOKEN_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'

def oauth_callback(code):
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
       'redirect_uri': IDENTITY_REDIRECT_URI,
    }
    auth = (IDENTITY_CLIENT_ID, IDENTITY_CLIENT_SECRET)
    response = requests.post(TOKEN_ENDPOINT, data=token_data, auth=auth)
    tokens = response.json()
    print(tokens)

if __name__ == '__main__':
    oauth_callback('your-authorization-code')