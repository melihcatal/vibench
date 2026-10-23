from identity_client import (
    auth_headers,
    build_client,
    build_query,
    normalize_identity_input,
)
from identity_models import PasswordResetRequest


def password_reset(email: str):
    req = PasswordResetRequest(**normalize_identity_input(email))
    with build_client() as client:
        resp = client.post(
            "/v1/accounts:sendOobCode",
            params=build_query(),
            headers=auth_headers(),
            json={"requestType": "PASSWORD_RESET", "email": req.email},
        )
    resp.raise_for_status()
    return resp.json()
