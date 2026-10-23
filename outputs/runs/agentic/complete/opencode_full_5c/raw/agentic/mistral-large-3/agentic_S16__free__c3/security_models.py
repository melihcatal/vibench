from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SecretResponse:
    """Standardized response for secret retrieval."""

    value: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class SecretRotationSummary:
    """Summary of secret rotation status."""

    secret_id: str
    current_version: str
    previous_version: Optional[str] = None
    rotation_status: str = "unknown"


def normalize_secret_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes secret payloads from different providers into a consistent format."""
    normalized = {
        "value": payload.get(
            "value",
            payload.get("SecretString", payload.get("payload", {}).get("data", "")),
        ),
        "version": payload.get(
            "version", payload.get("VersionId", payload.get("version_id"))
        ),
        "metadata": payload.get("metadata", {}),
    }
    return normalized
