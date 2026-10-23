import requests

def fetch_profile_claims(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    response.raise_for_status()
    return response.json()