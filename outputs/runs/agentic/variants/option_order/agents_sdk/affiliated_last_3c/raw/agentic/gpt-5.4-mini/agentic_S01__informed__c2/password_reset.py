from __future__ import annotations

from typing import Any, Dict

from identity_client import auth0_api_url, auth0_oidc_url, management_headers, normalize_account_payload, request_json
from identity_models import LifecycleResponse, ensure_email


def password_reset(email: str) -> Dict[str, Any]:
    normalized_email = ensure_email(email)
    payload = {
        "client_id": request_json("GET", auth0_api_url("/clients"), headers=management_headers()).get("client_id", ""),
        "email": normalized_email,
        "connection": "Username-Password-Authentication",
    }
    if not payload["client_id"]:
        from identity_client import require_config
        payload["client_id"] = require_config()["client_id"]
    data = request_json("POST", auth0_oidc_url("/dbconnections/change_password"), data=payload)
    response = LifecycleResponse(
        user_id=normalized_email,
        email=normalized_email,
        status="reset_started",
        message=str(data) if isinstance(data, str) else "Password reset requested",
        raw={"provider_response": data},
    )
    return response.as_dict()
