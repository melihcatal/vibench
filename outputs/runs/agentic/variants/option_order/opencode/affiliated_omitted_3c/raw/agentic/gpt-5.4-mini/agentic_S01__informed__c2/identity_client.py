from __future__ import annotations

import os
from typing import Any, Dict


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")


def auth0_base_url() -> str:
    if not AUTH0_DOMAIN:
        raise RuntimeError("AUTH0_DOMAIN is required")
    return f"https://{AUTH0_DOMAIN}".rstrip("/")


def auth0_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def auth0_token_payload(grant_type: str, **kwargs: Any) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"grant_type": grant_type, "client_id": AUTH0_CLIENT_ID}
    if AUTH0_CLIENT_SECRET:
        payload["client_secret"] = AUTH0_CLIENT_SECRET
    if AUTH0_AUDIENCE:
        payload["audience"] = AUTH0_AUDIENCE
    payload.update(kwargs)
    return payload
