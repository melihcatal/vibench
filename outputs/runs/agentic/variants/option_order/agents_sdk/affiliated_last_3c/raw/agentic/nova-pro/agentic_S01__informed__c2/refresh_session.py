import os
import requests

# Configuration
auth0_domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')
client_secret = os.getenv('AUTH0_CLIENT_SECRET')

# Refresh Session
def refresh_session(refresh_token):
    url = f'https://{auth0_domain}/oauth/token'
    payload = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()