import requests

from identity_client import get_identity_client


def oauth_callback(payload):
    client = get_identity_client()
    response = client.post('/oauth2/token', data=payload)
    response.raise_for_status()
    return response.json()