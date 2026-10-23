import os
from typing import Any, Dict, Optional

from identity_client import IdentityClient, build_user_payload, normalize_auth_result
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(request: RegisterUserRequest, *, client: Optional[IdentityClient] = None) -> RegisterUserResponse:
    identity_client = client or IdentityClient()
    payload = build_user_payload(request)
    response = identity_client.auth0.signup_email_password(payload)
    return normalize_auth_result(response, request.email)
