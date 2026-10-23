import os
import requests
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> LoginResponse:
    """Sign in a user with email and password and return tokens using Auth0."""
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not domain or not client_id:
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set"
        )

    url = f"https://{domain}/oauth/token"

    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "client_id": client_id,
        "audience": f"https://{domain}/api/v2/",
        "scope": "openid profile email",
    }

    headers = {"content-type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return LoginResponse(
            access_token=data.get("access_token"),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            expires_in=data.get("expires_in"),
            token_type=data.get("token_type"),
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to login with Auth0: {str(e)}")
