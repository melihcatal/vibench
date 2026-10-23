import requests

CLIENT_ID = 'your-client-id'
REDIRECT_URI = 'https://your-app.com/oauth_callback'
AUTHORIZATION_ENDPOINT = 'https://oauth.reddit.com/api/v1/authorize'

def start_oauth_login():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
       'redirect_uri': REDIRECT_URI,
        'scope': 'identity',
       'state': 'random_state_string'
    }
    authorization_url = f"{AUTHORIZATION_ENDPOINT}?client_id={CLIENT_ID}&response_type=code&state=random_state_string&redirect_uri={REDIRECT_URI}&scope=identity"
    print(f'Redirect to: {authorization_url}')

if __name__ == '__main__':
    start_oauth_login()