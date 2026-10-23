import os
import requests

def refresh_session(refresh_token):
    domain = os.getenv('AUTH0_DOMAIN')
    client_id = os.getenv('AUTH0_CLIENT_ID')
    client_secret = os.getenv('AUTH0_CLIENT_SECRET')

    response = requests.post(
        f'https://{domain}/oauth/token',
        json={
            'grant_type':'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token
        }
    )
    response.raise_for_status()
    return response.json()