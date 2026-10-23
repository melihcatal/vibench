import os
import requests

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

def fetch_profile_claims(access_token):
    userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(userinfo_url, headers=headers)
    profile = response.json()
    print(profile)