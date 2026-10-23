import os
import requests

def start_password_reset(email):
    domain = os.getenv('AUTH0_DOMAIN')
    client_id = os.getenv('AUTH0_CLIENT_ID')

    response = requests.post(
        f'https://{domain}/dbconnections/change_password',
        json={
            'client_id': client_id,
            'email': email
        }
    )
    response.raise_for_status()
    return response.json()