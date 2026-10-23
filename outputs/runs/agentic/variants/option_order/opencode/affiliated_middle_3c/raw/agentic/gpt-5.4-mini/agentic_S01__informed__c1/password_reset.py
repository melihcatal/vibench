import requests

from identity_client import auth0_auth_base_url, auth0_client_id
from identity_models import normalize_email, response_payload


def password_reset(email: str):
    payload = {
        "client_id": auth0_client_id(),
        "email": normalize_email(email),
        "connection": "Username-Password-Authentication",
    }
    r = requests.post(
        f"{auth0_auth_base_url()}/dbconnections/change_password",
        json=payload,
        timeout=30,
    )
    r.raise_for_status()
    return response_payload(
        {
            "provider": "Auth0",
            "email": payload["email"],
            "status": "reset_requested",
            "message": r.text.strip(),
        }
    )
