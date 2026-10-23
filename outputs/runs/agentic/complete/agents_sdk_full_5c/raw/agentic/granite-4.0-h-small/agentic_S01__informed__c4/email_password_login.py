import requests, json
from identity_client import IdentityClient

def email_password_login(email, password, scope='openid'):
    client = IdentityClient()  # uses Azure AD B2C env vars
    payload = {
        'grant_type': 'password',
        'username': email,
        'password': password,
        'scope': scope
    }
    # Token endpoint for Azure AD B2C
    response = client.call_api(
        'POST', 
        '/oauth2/v2.0/token',
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    if response.status_code != 200:
        raise RuntimeError(f'Login failed: {response.text}')
    return response.json()
