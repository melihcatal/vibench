import os
import requests

API_URL = 'https://api.auth0.com/v2/jobs/password-change'

def password_reset(email):
    headers = {
        'Authorization': 'Bearer ' + os.getenv('AUTH0_CLIENT_ID'),
        'Content-Type': 'application/json'
    }
    data = {
        'client_id': os.getenv('AUTH0_CLIENT_ID'),
        'connection': 'Username-Password-Authentication',
        'email': email
    }
    response = requests.post(API_URL, json=data, headers=headers)
    return response.json()