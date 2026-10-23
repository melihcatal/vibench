from __future__ import annotations

from identity_client import Auth0Client, load_auth0_config
from identity_models import PasswordResetRequest


def password_reset(email: str) -> dict:
    config = load_auth0_config()
    client = Auth0Client(config)
    request = PasswordResetRequest(email=email, connection=config.database_connection)
    response = client.post(
        "/dbconnections/change_password",
        request.to_auth0_payload(client_id=config.client_id),
    )
    return {
        "provider": "Auth0",
        "domain": config.domain,
        "email": email,
        "message": response if isinstance(response, str) else response.get("message", "password reset requested"),
    }
