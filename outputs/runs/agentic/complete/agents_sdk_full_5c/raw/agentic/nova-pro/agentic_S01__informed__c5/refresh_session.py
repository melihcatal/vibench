import os
import requests

API_URL = 'https://api.auth0.com/v2/token'

def refresh_session(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'client_id': os.getenv('AUTH0_CLIENT_ID'),
        'client_secret': os.getenv('AUTH0_CLIENT_SECRET'),
        'refresh_token': refresh_token
    }
    response = requests.post(API_URL, data=data)
    return response.json()