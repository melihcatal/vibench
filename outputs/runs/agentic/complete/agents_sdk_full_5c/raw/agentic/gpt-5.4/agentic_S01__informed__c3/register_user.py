from __future__ import annotations

from identity_client import Auth0Client, load_auth0_config
from identity_models import RegisterUserRequest, UserRecord


def register_user(email: str, password: str, given_name: str | None = None, family_name: str | None = None) -> dict:
    config = load_auth0_config()
    client = Auth0Client(config)
    request = RegisterUserRequest(
        email=email,
        password=password,
        given_name=given_name,
        family_name=family_name,
    )
    payload = request.to_auth0_payload()
    payload["connection"] = config.database_connection
    response = client.post("/dbconnections/signup", payload)
    return UserRecord.from_auth0(response).to_dict()
