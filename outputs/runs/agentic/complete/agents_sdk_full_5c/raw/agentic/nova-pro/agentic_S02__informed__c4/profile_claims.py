import os
import requests

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')

def get_profile(access_token):
    url = f'https://{AUTH0_DOMAIN}/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()