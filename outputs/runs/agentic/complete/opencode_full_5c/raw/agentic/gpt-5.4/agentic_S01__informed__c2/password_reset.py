from __future__ import annotations

from identity_client import auth0_client_id, auth0_db_connection, auth0_post
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> bool:
    payload = request.to_auth0_payload(auth0_client_id())
    payload["connection"] = request.connection or auth0_db_connection()
    auth0_post("/dbconnections/change_password", payload)
    return True
