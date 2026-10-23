from __future__ import annotations

from identity_client import auth0_client_id, auth0_db_connection, auth0_post
from identity_models import RegisterUserRequest, normalize_auth0_user, to_payload


def register_user(request: RegisterUserRequest):
    payload = {
        "client_id": auth0_client_id(),
        "email": request.email,
        "password": request.password,
        "connection": auth0_db_connection(),
    }
    user_metadata = {
        key: value
        for key, value in {
            "given_name": request.given_name,
            "family_name": request.family_name,
        }.items()
        if value
    }
    if user_metadata:
        payload["user_metadata"] = user_metadata
    response = auth0_post("/dbconnections/signup", payload)
    return normalize_auth0_user(
        response
        if response
        else to_payload(request) | {"user_id": "", "email_verified": False}
    )
