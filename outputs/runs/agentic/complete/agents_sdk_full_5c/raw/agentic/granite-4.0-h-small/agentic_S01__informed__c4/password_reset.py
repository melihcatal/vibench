import time, requests
from identity_client import IdentityClient

def start_password_reset(email):
    client = IdentityClient()
    payload = {
        'email': email,
        'send_reset_email': True
    }
    # Initiate password reset in Azure AD B2C
    response = client.call_api(
        'POST',
        '/b2c_1_reset_password',
        json=payload
    )
    if response.status_code != 200:
        raise RuntimeError(f'Password reset initiation failed: {response.text}')
    return response.json()
