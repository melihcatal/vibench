from __future__ import annotations

from typing import Any, Dict

from identity_client import get_client
from identity_models import LoginRequest, normalize_email


def email_password_login(request: LoginRequest | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(request, dict):
        request = LoginRequest(**request)
    client = get_client()
    return client.token(
        "password",
        username=normalize_email(request.email),
        password=request.password,
        audience=client.config.management_audience,
        scope="openid profile email offline_access",
    )
