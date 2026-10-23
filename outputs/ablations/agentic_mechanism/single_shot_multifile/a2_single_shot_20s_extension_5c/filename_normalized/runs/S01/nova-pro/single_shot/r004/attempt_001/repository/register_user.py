import requests
import os
from [HELPER] identity_client import auth0_management_api_client

def register_user(email, password):
    client = auth0_management_api_client()
    response = client.post('/api/v2/users', json={
        'email': email,
        'password': password,
        'connection': 'Username-Password-Authentication'
    })
    response.raise_for_status()
    return response.json()
