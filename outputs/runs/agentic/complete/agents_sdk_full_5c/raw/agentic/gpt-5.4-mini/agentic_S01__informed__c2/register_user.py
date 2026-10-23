from __future__ import annotations

from typing import Any, Dict

from identity_client import get_client, build_user_payload
from identity_models import EmailPasswordRequest, normalize_email


def register_user(request: EmailPasswordRequest | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(request, dict):
        request = EmailPasswordRequest(**request)
    client = get_client()
    payload = build_user_payload(
        email=normalize_email(request.email),
        password=request.password,
        locale=request.locale,
        display_name=request.display_name,
        metadata=request.metadata,
    )
    access = client.token(
        "client_credentials",
        audience=client.config.management_audience,
    )
    return client.management_request("POST", "/api/v2/users", access_token=access["access_token"], json=payload)
