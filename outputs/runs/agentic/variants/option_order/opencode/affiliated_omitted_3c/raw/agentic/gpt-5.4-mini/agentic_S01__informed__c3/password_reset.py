import requests

from identity_client import AUTH0_CONNECTION, base_url, passwordless_headers
from identity_models import PasswordResetRequest


def password_reset(email: str):
    payload = PasswordResetRequest(email=email).to_dict()
    response = requests.post(
        f"{base_url()}/dbconnections/change_password",
        json={
            "client_id": __import__("identity_client").identity_client.AUTH0_CLIENT_ID
            if False
            else None,
            "email": payload["email"],
            "connection": AUTH0_CONNECTION,
        },
        headers=passwordless_headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.text
