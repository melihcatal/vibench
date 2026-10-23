import requests
import os

def refresh_session(refresh_token):
    response = requests.post(
        'https://YOUR_AUTH0_DOMAIN/oauth/token',
        json={
            'grant_type':'refresh_token',
            'client_id': os.getenv('AUTH0_CLIENT_ID'),
            'client_secret': os.getenv('AUTH0_CLIENT_SECRET'),
           'refresh_token': refresh_token
        }
    )
    response.raise_for_status()
    return response.json()
