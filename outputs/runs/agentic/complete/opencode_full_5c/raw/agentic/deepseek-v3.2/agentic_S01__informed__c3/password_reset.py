import os
import requests


def password_reset(
    email: str, connection: str = "Username-Password-Authentication"
) -> dict:
    """Start a password reset flow for a local account using Auth0."""
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not domain or not client_id:
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set"
        )

    url = f"https://{domain}/dbconnections/change_password"

    payload = {"client_id": client_id, "email": email, "connection": connection}

    headers = {"content-type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        return {"success": True, "message": "Password reset email sent", "email": email}
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to initiate password reset with Auth0: {str(e)}")
