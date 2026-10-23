import os
import requests

API_URL = 'https://api.auth0.com/v2/token'

def email_password_login(email, password):
    data = {
        'grant_type': 'password',
        'client_id': os.getenv('AUTH0_CLIENT_ID'),
        'client_secret': os.getenv('AUTH0_CLIENT_SECRET'),
        'username': email,
        'password': password,
        'scope': 'openid profile email',
        'audience': 'https://your-api-audience'
    }
    response = requests.post(API_URL, data=data)
    return response.json()