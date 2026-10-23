import os
from identity_client import IdentityClient

def email_password_login(email: str, password: str):
    """Sign in a user with email and password and return JWT access/refresh tokens.
    Auth0 generates the tokens; this wrapper extracts them from the response.
    Raises RuntimeError on login failure.
    """
    payload = {
        "email": email.lower(),
        "password": password,
        "connection": "Username-Password-Authentication",
    }
    client = IdentityClient()
    response = client.login(payload)
    if response.get('access_token') and response.get('refresh_token'):
        return {
            "access_token": response['access_token'],
            "refresh_token": response['refresh_token'],
            "id_token": response.get('id_token')
        }
    raise RuntimeError(f"Login failed: {response}")
