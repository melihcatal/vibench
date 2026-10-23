import requests
import os

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
USERINFO_URL = 'https://openidconnect.googleapis.com/v1/userinfo'

def fetch_profile(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(USERINFO_URL, headers=headers)
    response.raise_for_status()
    return response.json()