import os
import requests

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')

def fetch_profile_claims(access_token):
    userinfo_url = f'https://{AUTH0_DOMAIN}/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(userinfo_url, headers=headers)
    return response.json()