import requests
from typing import Dict, Any
import os


def email_password_login(email: str, password: str) -> Dict[str, Any]:
    """
    Signs in a user with email and password using Auth0 Authentication API.

    Args:
        email: User email address
        password: User password

    Returns:
        Dictionary containing access token, refresh token, and user info
    """
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    audience = os.getenv("AUTH0_AUDIENCE")

    token_url = f"https://{auth0_domain}/oauth/token"

    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": audience,
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()

    token_data = response.json()

    # Fetch user info using the access token
    user_info_url = f"https://{auth0_domain}/userinfo"
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    user_response = requests.get(user_info_url, headers=headers)
    user_response.raise_for_status()

    return {
        "access_token": token_data["access_token"],
        "refresh_token": token_data.get("refresh_token"),
        "expires_in": token_data["expires_in"],
        "user_info": user_response.json(),
        "provider": "auth0",
    }
