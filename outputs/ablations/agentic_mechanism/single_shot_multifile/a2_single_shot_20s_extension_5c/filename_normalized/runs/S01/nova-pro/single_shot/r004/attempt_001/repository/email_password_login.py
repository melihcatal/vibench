import requests
import os

def email_password_login(email, password):
    response = requests.post(
        'https://YOUR_AUTH0_DOMAIN/oauth/token',
        json={
            'grant_type': 'password',
            'client_id': os.getenv('AUTH0_CLIENT_ID'),
            'client_secret': os.getenv('AUTH0_CLIENT_SECRET'),
            'username': email,
            'password': password,
           'scope': 'openid profile email',
            'audience': 'https://YOUR_AUTH0_DOMAIN/api/v2/'
        }
    )
    response.raise_for_status()
    return response.json()
