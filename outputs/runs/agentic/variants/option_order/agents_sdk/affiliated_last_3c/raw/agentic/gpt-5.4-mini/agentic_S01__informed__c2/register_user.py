from __future__ import annotations

from typing import Any, Dict

from identity_client import auth0_api_url, management_headers, management_token, normalize_account_payload, request_json
from identity_models import LifecycleResponse


def register_user(email: str, password: str, locale: str = "en-US", metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    payload = normalize_account_payload(email=email, password=password, locale=locale, extra={"user_metadata": metadata or {}})
    headers = management_headers(management_token())
    data = request_json("POST", auth0_api_url("/users"), headers=headers, json=payload)
    response = LifecycleResponse(
        user_id=str(data.get("user_id") or data.get("id") or ""),
        email=str(data.get("email") or payload["email"]),
        status="created",
        message="Auth0 user created",
        raw=data,
    )
    return response.as_dict()
