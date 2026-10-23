import os
import requests

# Load Auth0 credentials from environment
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

# Auth0 Management API endpoint for password reset initiation
RESET_URL = f'https://{AUTH0_DOMAIN}/api/v2/passwords/change`

def password_reset(email: str, connection: str = 'Username-Password-Authentication') -> dict:
    """Start a password reset flow for a local account using Auth0 Management API.
    Sends a verification email to the user.
    Returns the API response.
    """
    token = f'Bearer {AUTH0_CLIENT_ID}:{AUTH0_CLIENT_SECRET}'
    headers = {'Authorization': token}
    payload = {
        'client_id': AUTH0_CLIENT_ID,
        'email': email,
        'connection': connection,
        'send_email': True
    }
    response = requests.post(RESET_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
