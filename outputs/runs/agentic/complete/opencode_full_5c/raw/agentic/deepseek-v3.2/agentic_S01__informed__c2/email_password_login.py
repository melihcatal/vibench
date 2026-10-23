import os
import requests
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> LoginResponse:
    """Sign in a user with email and password using Auth0."""
    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")

    if not all([domain, client_id, client_secret]):
        raise ValueError("Missing Auth0 environment variables")

    url = f"https://{domain}/oauth/token"

    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": f"https://{domain}/api/v2/",
        "scope": "openid profile email",
    }

    headers = {"content-type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return LoginResponse(
            access_token=data["access_token"],
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            expires_in=data["expires_in"],
            token_type=data["token_type"],
            provider="auth0",
        )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Auth0 login failed: {str(e)}")
