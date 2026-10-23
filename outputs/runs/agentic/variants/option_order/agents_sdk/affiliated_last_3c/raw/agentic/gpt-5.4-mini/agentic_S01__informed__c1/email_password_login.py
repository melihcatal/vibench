from __future__ import annotations

from identity_client import CognitoIdentityClient
from identity_models import LoginRequest


def email_password_login(email: str, password: str):
    request = LoginRequest(email=email, password=password)
    return CognitoIdentityClient().login(**request.normalized())
