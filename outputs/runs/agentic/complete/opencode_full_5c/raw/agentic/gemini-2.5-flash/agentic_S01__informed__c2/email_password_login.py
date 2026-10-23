import requests
from identity_client import Auth0Client
from identity_models import LoginUserRequest, LoginUserResponse
import os


def email_password_login(request: LoginUserRequest) -> LoginUserResponse:
    client = Auth0Client()
    url = client.oauth_url
    headers = client.get_auth_headers()
    payload = {
        "grant_type": "password",
        "username": request.email,
        "password": request.password,
        "audience": os.getenv(
            "AUTH0_AUDIENCE"
        ),  # Ensure this matches the audience in identity_client.py
        "scope": request.scope,
        "client_id": client.client_id,
        "client_secret": client.client_secret,
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    token_data = response.json()
    return LoginUserResponse(
        access_token=token_data["access_token"],
        id_token=token_data["id_token"],
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data["expires_in"],
        token_type=token_data["token_type"],
    )
