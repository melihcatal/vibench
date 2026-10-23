from __future__ import annotations

from identity_client import CognitoIdentityClient
from identity_models import RegisterUserRequest


def register_user(email: str, password: str, given_name: str | None = None, family_name: str | None = None, locale: str | None = None):
    request = RegisterUserRequest(
        email=email,
        password=password,
        given_name=given_name,
        family_name=family_name,
        locale=locale,
    )
    return CognitoIdentityClient().register_user(**request.normalized())
