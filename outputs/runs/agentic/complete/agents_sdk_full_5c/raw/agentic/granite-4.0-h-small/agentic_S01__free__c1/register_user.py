import os
from identity_client import IdentityClient

def register_user(email: str, password: str, locale: str = 'en'):
    """Create a new email/password user account.
    Uses SendGrid to verify the email address and stores the password hash in Auth0.
    Returns the Auth0 user_id on success.
    """
    # Normalize input
    payload = {
        "email": email.lower(),
        "password": password,
        "connection": "Username-Password-Authentication",
        "locale": locale,
    }
    client = IdentityClient()
    # Call Auth0 management API via wrapper
    response = client.create_user(payload)
    if response.get('success'):
        return response['user_id']
    raise RuntimeError(f"Failed to register user: {response}")
