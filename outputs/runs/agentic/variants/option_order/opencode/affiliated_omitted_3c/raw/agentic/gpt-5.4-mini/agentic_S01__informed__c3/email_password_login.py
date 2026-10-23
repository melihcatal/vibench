import requests

from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_CONNECTION,
    base_url,
    passwordless_headers,
)
from identity_models import LoginRequest


def email_password_login(email: str, password: str):
    payload = LoginRequest(email=email, password=password).to_dict()
    response = requests.post(
        f"{base_url()}/oauth/token",
        json={
            "grant_type": "password",
            "username": payload["email"],
            "password": payload["password"],
            "client_id": AUTH0_CLIENT_ID,
            "connection": AUTH0_CONNECTION,
        },
        headers=passwordless_headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
