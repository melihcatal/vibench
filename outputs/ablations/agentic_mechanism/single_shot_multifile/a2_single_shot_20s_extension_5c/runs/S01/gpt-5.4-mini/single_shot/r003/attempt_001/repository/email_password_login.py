from typing import Optional

from identity_client import IdentityClient, build_login_payload, normalize_auth_result
from identity_models import LoginRequest, LoginResponse


def email_password_login(request: LoginRequest, *, client: Optional[IdentityClient] = None) -> LoginResponse:
    identity_client = client or IdentityClient()
    payload = build_login_payload(request)
    response = identity_client.auth0.login_email_password(payload)
    return normalize_auth_result(response, request.email)
