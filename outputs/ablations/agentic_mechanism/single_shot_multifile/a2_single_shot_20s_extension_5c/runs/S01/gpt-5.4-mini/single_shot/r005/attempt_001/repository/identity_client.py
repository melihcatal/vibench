import os
from typing import Any


_PROVIDER_HOSTNAME = "identitytoolkit.googleapis.com"


def build_identity_base_url() -> str:
    api_key = os.getenv("FIREBASE_WEB_API_KEY") or os.getenv("GOOGLE_CLOUD_API_KEY")
    if not api_key:
        raise RuntimeError("FIREBASE_WEB_API_KEY or GOOGLE_CLOUD_API_KEY is required")
    return f"https://{_PROVIDER_HOSTNAME}/v1"


def json_headers() -> dict[str, str]:
    return {"Content-Type": "application/json"}


def normalize_identity_error(response: Any) -> str:
    try:
        payload = response.json()
    except Exception:
        return f"identity provider error: {response.status_code}"
    error = payload.get("error", {}) if isinstance(payload, dict) else {}
    message = error.get("message") or payload.get("message") if isinstance(payload, dict) else None
    return message or f"identity provider error: {response.status_code}"
