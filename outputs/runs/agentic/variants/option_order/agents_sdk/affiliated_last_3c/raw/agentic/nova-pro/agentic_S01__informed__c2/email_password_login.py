import os
import requests

# Configuration
auth0_domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')

# Email/Password Login
def email_password_login(email, password):
    url = f'https://{auth0_domain}/oauth/token'
    payload = {
        'grant_type': 'password',
        'username': email,
        'password': password,
        'client_id': client_id,
        'audience': f'https://{auth0_domain}/api/v2/',
        'scope': 'openid profile email'
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()