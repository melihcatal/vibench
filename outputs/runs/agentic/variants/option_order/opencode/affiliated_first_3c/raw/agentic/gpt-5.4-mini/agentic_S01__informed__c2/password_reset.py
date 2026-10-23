import requests

from identity_client import Auth0Client
from identity_models import PasswordResetRequest


def password_reset(email: str):
    client = Auth0Client()
    payload = PasswordResetRequest(email=client.normalize(email))
    response = requests.post(
        f"{client.base_url}/dbconnections/change_password",
        json={
            "client_id": client.client_id,
            "email": payload.email,
            "connection": "Username-Password-Authentication",
        },
        headers=client.headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.text
