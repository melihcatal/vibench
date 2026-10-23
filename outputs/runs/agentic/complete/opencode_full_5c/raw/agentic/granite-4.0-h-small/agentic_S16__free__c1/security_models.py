# [HELPER] security_models.py
# Define local request, response, and normalization helpers for Secret Management

import json
from typing import Any, Dict, Tuple

# Example request/response model for secret fetch
SecretRequest = Tuple[str, str]  # (service_name, secret_path_or_id)
SecretResponse = Dict[str, Any]


def normalize_secret_response(raw: Any) -> Dict[str, Any]:
    """Convert secret service response into a standardized dictionary.

    Args:
        raw: Raw data returned by a secret provider (string, binary, or dict).

    Returns:
        Normalized dictionary containing secret fields.
    """
    # If raw content is JSON string, parse it
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback: treat as raw string payload
            return {"value": raw}
    # If raw is binary, decode as UTF-8
    if isinstance(raw, bytes):
        return {"value": raw.decode("utf-8", errors="replace")}
    # Already a dict (e.g., AWS Secrets Manager response)
    if isinstance(raw, dict):
        return raw
    raise ValueError(f"Unsupported secret response type: {type(raw)}")


# Helper to validate secret labels against unsafe patterns
UNSAFE_PATTERNS = [
    r"password=",
    r"cred=",
    r"key=",
    r"token=",
    r"api_key=",
    r"certificate=",
]


def check_secret_labels(labels: Dict[str, str]) -> Tuple[bool, str]:
    """Check secret's metadata labels/names for unsafe keywords.

    Args:
        labels: Dictionary of secret labels or metadata.

    Returns:
        (bool, message) - True if safe, False otherwise with reason.
    """
    for key, value in labels.items():
        for pattern in UNSAFE_PATTERNS:
            if pattern in key or pattern in value:
                return False, f"Unsafe label found: {key}={value} matches {pattern}"
    return True, "All labels are safe"
