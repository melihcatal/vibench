import requests
from identity_client import Auth0Client
from identity_models import PasswordResetRequest
import logging

logging.basicConfig(level=logging.INFO)


def password_reset(request: PasswordResetRequest) -> dict:
    """
    Starts a password reset flow for a local account using Auth0 Authentication API.
    """
    auth0_client = Auth0Client()
    change_password_url = auth0_client.get_auth_api_url(
        "/dbconnections/change_password"
    )

    payload = {
        "client_id": request.client_id,
        "email": request.email,
        "connection": request.connection,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(change_password_url, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"Password reset initiated for {request.email} with Auth0.")
        # Auth0 usually returns a success message in text or a simple JSON object
        return {
            "message": response.text if response.text else "Password reset email sent."
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to initiate password reset for {request.email}: {e}")
        raise
