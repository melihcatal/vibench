import os
import requests
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> LoginResponse:
    """Authenticate user with email and password using Auth0."""
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    # Auth0 OAuth token endpoint for password grant
    token_url = f"https://{domain}/oauth/token"

    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": f"https://{domain}/api/v2/",
        "scope": "openid profile email",
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()

    token_data = response.json()

    # Get user info using access token
    userinfo_url = f"https://{domain}/userinfo"
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    userinfo_response = requests.get(userinfo_url, headers=headers)
    userinfo_response.raise_for_status()
    user_info = userinfo_response.json()

    return LoginResponse(
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        id_token=token_data.get("id_token"),
        expires_in=token_data["expires_in"],
        token_type=token_data["token_type"],
        user_id=user_info.get("sub"),
        email=user_info.get("email"),
    )
