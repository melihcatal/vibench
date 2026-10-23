import requests

from identity_client import AUTH0_CONNECTION, base_url, management_headers
from identity_models import RegisterUserRequest


def register_user(email: str, password: str, locale: str = "en-US"):
    payload = RegisterUserRequest(
        email=email, password=password, locale=locale
    ).to_dict()
    response = requests.post(
        f"{base_url()}/api/v2/users",
        json={
            "email": payload["email"],
            "password": payload["password"],
            "connection": AUTH0_CONNECTION,
            "user_metadata": {"locale": payload["locale"]},
        },
        headers=management_headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
