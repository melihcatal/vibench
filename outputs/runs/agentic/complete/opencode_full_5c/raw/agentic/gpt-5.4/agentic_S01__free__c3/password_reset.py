from __future__ import annotations

from identity_client import auth0_client_id, auth0_db_connection, auth0_post
from identity_models import PasswordResetRequest, normalize_password_reset


def password_reset(request: PasswordResetRequest):
    payload = {
        "client_id": auth0_client_id(),
        "email": request.email,
        "connection": request.connection or auth0_db_connection(),
    }
    response = auth0_post("/dbconnections/change_password", payload)
    if isinstance(response, dict):
        raw = response
    else:
        raw = {"message": str(response)}
    return normalize_password_reset(request.email, raw)
