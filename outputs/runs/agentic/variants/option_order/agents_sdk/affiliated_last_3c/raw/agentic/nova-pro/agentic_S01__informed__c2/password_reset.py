import os
import requests

# Configuration
auth0_domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')

# Password Reset
def password_reset(email):
    url = f'https://{auth0_domain}/dbconnections/change_password'
    payload = {
        'client_id': client_id,
        'email': email
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()