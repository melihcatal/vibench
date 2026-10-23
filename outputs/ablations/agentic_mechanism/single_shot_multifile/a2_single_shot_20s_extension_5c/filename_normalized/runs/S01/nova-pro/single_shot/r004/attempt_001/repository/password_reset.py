import requests
import os

def start_password_reset(email):
    response = requests.post(
        'https://YOUR_AUTH0_DOMAIN/dbconnections/change_password',
        json={
            'client_id': os.getenv('AUTH0_CLIENT_ID'),
            'email': email
        }
    )
    response.raise_for_status()
    return response.json()
