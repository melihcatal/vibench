from __future__ import annotations

from identity_client import auth0_db_connection, auth0_management_token, auth0_post
from identity_models import RegisterUserRequest, UserAccount, normalize_auth0_user


def register_user(request: RegisterUserRequest) -> UserAccount:
    payload = request.to_auth0_payload()
    payload["connection"] = request.connection or auth0_db_connection()
    response = auth0_post(
        "/api/v2/users", payload, bearer_token=auth0_management_token()
    )
    return normalize_auth0_user(response)
