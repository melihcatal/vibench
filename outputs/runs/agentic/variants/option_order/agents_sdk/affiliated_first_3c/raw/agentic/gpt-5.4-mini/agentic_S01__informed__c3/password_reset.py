from __future__ import annotations

from identity_client import auth0_client_id, auth0_reset_connection, get_client
from identity_models import PasswordResetRequest, normalize_email


def start_password_reset(email: str) -> dict:
    client = get_client()
    req = PasswordResetRequest(email=normalize_email(email), connection=auth0_reset_connection())
    response = client.session.post(
        f"{client.oauth_base}/dbconnections/change_password",
        json={
            "client_id": auth0_client_id(),
            "email": req.email,
            "connection": req.connection,
        },
        timeout=30,
    )
    response.raise_for_status()
    return {"email": req.email, "provider": "auth0", "message": response.text}
