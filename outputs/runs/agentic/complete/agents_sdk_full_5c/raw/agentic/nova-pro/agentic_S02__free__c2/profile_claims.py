import requests
from identity_client import get_auth0_client

def get_profile_claims(access_token):
    client = get_auth0_client()
    userinfo_url = f'https://{client.domain}/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(userinfo_url, headers=headers)
    return response.json()