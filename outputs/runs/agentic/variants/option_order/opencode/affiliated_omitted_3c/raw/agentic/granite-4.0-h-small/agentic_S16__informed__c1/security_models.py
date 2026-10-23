import json
from typing import Any, Dict

# Normalization helpers for secret payloads


def normalize_secret(secret: Dict[str, Any]) -> Dict[str, Any]:
    """Convert secret dict to a standardized shape.
    Ensures presence of 'username', 'password', and 'endpoint' fields.
    """
    normalized = {
        "username": secret.get("username") or secret.get("user") or None,
        "password": secret.get("password") or None,
        "endpoint": secret.get("host") or secret.get("endpoint") or None,
        "extra": {
            k: v
            for k, v in secret.items()
            if k not in ("username", "user", "password", "host", "endpoint")
        },
    }
    return normalized


def serialize_for_audit(payload: Any) -> str:
    """Serialize arbitrary audit notes to a JSON string, stripping sensitive keys.
    Sensitive keys ('password', 'secret', 'token') are omitted.
    """
    sensitive_keys = {"password", "secret", "token", "apikey", "key"}
    cleaned = {k: v for k, v in payload.items() if k not in sensitive_keys}
    return json.dumps(cleaned, indent=2)
