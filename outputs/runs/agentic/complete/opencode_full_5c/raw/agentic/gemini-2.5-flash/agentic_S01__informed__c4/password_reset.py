import requests
from identity_client import auth0_client
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> dict:
    """Starts a password reset flow for a local account using Auth0 Authentication API."""
    payload = {
        "client_id": auth0_client.client_id,
        "email": request.email,
        "connection": request.connection,
    }

    try:
        response = requests.post(auth0_client.password_reset_url, json=payload)
        response.raise_for_status()
        # Auth0 returns a success message in text format for this endpoint
        return {"message": response.text}
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Auth0 password reset failed: {e}")
