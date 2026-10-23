import requests
from identity_client import get_client

def profile_claims(access_token):
    client = get_client()
    profile_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(profile_url, headers=headers)
    profile = response.json()
    print('Profile:', profile)