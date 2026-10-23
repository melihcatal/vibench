import time, requests
from identity_client import IdentityClient

def refresh_session(refresh_token):
    client = IdentityClient()
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': 'openid profile'
    }
    # Token endpoint for Azure AD B2C
    response = client.call_api(
        'POST',
        '/oauth2/v2.0/token',
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    if response.status_code != 200:
        raise RuntimeError(f'Refresh failed: {response.text}')
    return response.json()
