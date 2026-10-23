import requests, json
from identity_client import IdentityClient

def register_user(email, password, **extra):
    # Configure provider credentials
    client = IdentityClient()  # loads env vars for Azure AD B2C
    # Build payload for registration
    payload = {
        'email': email,
        'password': password,
        **extra
    }
    # Call provider API (Azure AD B2C) for user registration
    response = client.call_api(
        'POST', 
        '/b2c_1_sign_up', 
        json=payload
    )
    # Validate response
    if response.status_code != 201:
        raise RuntimeError(f'Registration failed: {response.text}')
    return response.json()
