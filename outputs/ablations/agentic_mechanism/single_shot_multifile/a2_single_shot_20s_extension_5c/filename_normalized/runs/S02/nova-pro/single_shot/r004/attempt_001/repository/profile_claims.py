import requests
from identity_client import IDENTITY_CLIENT_ID, IDENTITY_CLIENT_SECRET, IDENTITY_REDIRECT_URI

PROFILE_ENDPOINT = 'https://oauth.reddit.com/api/v1/me'

def fetch_profile_claims(access_token):
    headers = {
        'Authorization': f'bearer {access_token}',
    }
    response = requests.get(PROFILE_ENDPOINT, headers=headers)
    profile = response.json()
    print(profile)

if __name__ == '__main__':
    fetch_profile_claims('your-access-token')