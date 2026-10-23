import os
import requests
from identity_client import IdentityClient

def email_password_login(email: str, password: str):
    """Sign in a user with email and password using Auth0 OAuth /oauth/token endpoint.

    Returns JSON with 'access_token', 'id_token', and 'refresh_token' on success.
    Raises for invalid credentials or API errors.
    """
    client = IdentityClient()
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "audience": client.auth0_api_audience,
        "scope": "openid profile email",
        "client_id": client.auth0_client_id,
        "client_secret": client.auth0_client_secret,
    }
    response = requests.post(
        f"{client.auth0_domain}/oauth/token",
        data=payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
