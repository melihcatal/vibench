import requests

from identity_client import get_identity_client


def profile_claims(token):
    client = get_identity_client()
    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/userinfo', headers=headers)
    response.raise_for_status()
    return response.json()