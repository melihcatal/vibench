import os
import requests

API_URL = 'https://api.auth0.com/v2/users'

def register_user(email, password):
    headers = {
        'Authorization': 'Bearer ' + os.getenv('AUTH0_CLIENT_ID'),
        'Content-Type': 'application/json'
    }
    data = {
        'email': email,
        'password': password,
        'connection': 'Username-Password-Authentication'
    }
    response = requests.post(API_URL, json=data, headers=headers)
    return response.json()