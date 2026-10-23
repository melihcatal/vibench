import os
import requests
from identity_client import Auth0Client
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> PasswordResetResponse:
    client = Auth0Client()
    url = f"https://{client.domain}/dbconnections/change_password"
    payload = PasswordResetRequest(email=email, client_id=client.client_id).dict()

    response = requests.post(url, json=payload, headers=client.headers)
    response.raise_for_status()
    data = response.json()

    return PasswordResetResponse(
        status="success", message=data.get("message", "Password reset email sent")
    )
