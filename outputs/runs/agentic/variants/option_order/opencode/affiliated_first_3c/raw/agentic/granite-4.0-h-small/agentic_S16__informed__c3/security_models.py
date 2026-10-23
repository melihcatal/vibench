# security_models.py
# [HELPER]
# Define local request, response, and normalization helpers for Secret Management

import json
from typing import Dict, Any, Union


# Standard error wrapper
class SecretError(Exception):
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(message)
        self.details = details or {}


# Normalized secret response model (after fetching raw data)
class SecretResponse:
    def __init__(self, name: str, version_id: str, data: Union[Dict[str, Any], str]):
        self.name = name  # secret name/identifier
        self.version_id = version_id  # version identifier used
        self.data = data  # parsed data (dict if JSON, else string)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "version_id": self.version_id, "data": self.data}


# Helper to normalize raw provider responses into SecretResponse instances


def normalize_response(provider_name: str, raw: Any) -> SecretResponse:
    """Convert raw API responses (AWS, IBM, Alibaba, Google) into a common model.

    Args:
        provider_name: Identifier used for logging/debugging.
        raw: Raw result from the provider (dict or string).

    Returns:
        A SecretResponse containing normalized fields.
    """
    # Assume the raw payload is either a dict (JSON) or raw string
    try:
        content = json.loads(raw) if isinstance(raw, str) else raw
    except json.JSONDecodeError:
        content = raw  # treat as raw string (e.g., binary secret)

    if provider_name == "aws":
        # AWS returns SecretString (plaintext) or binary SecretBinary
        name = raw.get("Name", "unknown")
        version_id = raw.get("VersionId", "unknown")
        data = content.get("SecretString") or raw.get("SecretBinary")
    elif provider_name == "ibm":
        # IBM Secrets Manager returns plaintext in get_secret().result()['plaintext']
        name = raw.get("name", "unknown")
        version_id = raw.get("version_id", "latest")
        data = content  # already plaintext string
    elif provider_name == "alibaba":
        # Alibaba returns plaintext directly
        name = raw.get("SecretName", "unknown")
        version_id = raw.get("VersionId", "latest")
        data = content
    elif provider_name == "google":
        # Google returns payload.data as plaintext bytes
        name = raw.metadata.secret_name
        version_id = raw.name.split("/versions/")[-1]
        data = content.decode("UTF-8")
    else:
        # Fallback for other providers (e.g., Azure, Doppler)
        name = raw.get("name", "unknown")
        version_id = raw.get("version", "latest")
        data = raw.get("payload", raw)

    return SecretResponse(name, version_id, data)
