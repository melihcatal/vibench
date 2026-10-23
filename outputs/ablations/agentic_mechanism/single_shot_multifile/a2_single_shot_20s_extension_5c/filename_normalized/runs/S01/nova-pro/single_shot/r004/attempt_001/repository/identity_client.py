import requests
import os

def auth0_management_api_client():
    token_response = requests.post(
        'https://YOUR_AUTH0_DOMAIN/oauth/token',
        json={
            'client_id': os.getenv('AUTH0_CLIENT_ID'),
            'client_secret': os.getenv('AUTH0_CLIENT_SECRET'),
            'audience': 'https://YOUR_AUTH0_DOMAIN/api/v2/',
            'grant_type': 'client_credentials'
        }
    )
    token_response.raise_for_status()
    access_token = token_response.json().get('access_token')
    return requests.Session().headers.update({'Authorization': f'Bearer {access_token}')
