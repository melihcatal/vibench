import requests

from identity_client import auth0_url, load_identity_config, normalize_email
from identity_models import PasswordResetRequest, to_payload


def start_password_reset(email: str):
    config = load_identity_config()
    payload = to_payload(
        PasswordResetRequest(
            email=normalize_email(email),
            connection=config.auth0_reset_connection,
        )
    )
    response = requests.post(
        auth0_url(config.auth0_domain, "/dbconnections/change_password"),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return {"status": "sent", "message": response.text}
