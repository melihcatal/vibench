import requests

AUTH0_DOMAIN = 'dev-123456.us.auth0.com'

def start_oauth_login():
    auth_url = f'https://{AUTH0_DOMAIN}/authorize'
    params = {
        'audience': 'https://myapi',
        'response_type': 'code',
        'client_id': 'YOUR_AUTH0_CLIENT_ID',
        'redirect_uri': 'https://yourapp.com/callback',
        'scope': 'openid profile email'
    }
    response = requests.get(auth_url, params=params)
    return response.url