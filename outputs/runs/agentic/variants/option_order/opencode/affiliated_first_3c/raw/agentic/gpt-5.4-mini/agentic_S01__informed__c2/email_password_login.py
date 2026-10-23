import requests

from identity_client import Auth0Client
from identity_models import LoginRequest, as_dict


def email_password_login(email: str, password: str):
    client = Auth0Client()
    payload = LoginRequest(email=client.normalize(email), password=password)
    response = requests.post(
        f"{client.base_url}/oauth/token",
        json={
            "grant_type": "password",
            "client_id": client.client_id,
            "username": payload.email,
            "password": payload.password,
            "scope": "openid profile email offline_access",
            "audience": client.audience or f"https://{client.domain}/api/v2/",
        },
        headers=client.headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
