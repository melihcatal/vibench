import os
import requests

def email_password_login(email, password):
    domain = os.getenv('AUTH0_DOMAIN')
    client_id = os.getenv('AUTH0_CLIENT_ID')

    response = requests.post(
        f'https://{domain}/oauth/token',
        json={
            'grant_type': 'password',
            'username': email,
            'password': password,
            'client_id': client_id,
            'audience': f'https://{domain}/api/v2/',
           'scope': 'openid profile email'
        }
    )
    response.raise_for_status()
    return response.json()