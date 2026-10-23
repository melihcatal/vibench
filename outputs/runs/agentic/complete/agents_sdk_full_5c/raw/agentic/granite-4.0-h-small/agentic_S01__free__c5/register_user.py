import os
import requests
from identity_client import IdentityClient

def register_user(email: str, password: str, first_name: str = '', last_name: str = ''):
    """Create a new email/password user account using Auth0.\n\n    Returns the user object from Auth0 on success, raises for errors.\n    """
    client = IdentityClient()
    payload = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
        "user_metadata": {
            "first_name": first_name,
            "last_name": last_name,
        },
    }
    response = requests.post(
        f"{client.auth0_domain}/api/v2/users",
        json=payload,
        headers={"Authorization": f"Bearer {client.auth0_management_token}"},
        timeout=10
    )
    response.raise_for_status()
    return response.json()
