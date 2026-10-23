import httpx

from identity_client import (
    auth_headers,
    build_client,
    build_query,
    normalize_identity_input,
)
from identity_models import RegisterUserRequest, response_payload


def register_user(email: str, password: str):
    req = RegisterUserRequest(**normalize_identity_input(email, password))
    with build_client() as client:
        resp = client.post(
            "/v1/accounts:signUp",
            params=build_query(),
            headers=auth_headers(),
            json={
                "email": req.email,
                "password": req.password,
                "returnSecureToken": True,
            },
        )
    resp.raise_for_status()
    return response_payload(resp.json())
