import os
import requests

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
USERINFO_URL = 'https://openidconnect.googleapis.com/v1/userinfo'

def fetch_profile_claims(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    response = requests.get(USERINFO_URL, headers=headers)
    profile = response.json()
    return profile
