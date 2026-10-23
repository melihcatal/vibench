import os
import requests
from identity_client import AUTH0_DOMAIN, AUTH0_CLIENT_ID
from identity_models import PasswordResetRequest


def password_reset(email: str) -> dict:
    """
    Starts a password reset flow for a local Auth0 account.
    """
    change_password_url = f"https://{AUTH0_DOMAIN}/dbconnections/change_password"
    headers = {"Content-Type": "application/json"}
    password_reset_request = PasswordResetRequest(
        email=email, client_id=AUTH0_CLIENT_ID
    )

    response = requests.post(
        change_password_url, headers=headers, json=password_reset_request.to_dict()
    )
    response.raise_for_status()
    return {"message": response.text}  # Auth0 returns a simple message on success
