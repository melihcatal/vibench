from __future__ import annotations
from typing import Dict, List, Optional


class SecretMeta:
    """Normalization container for secret metadata returned from any provider.",

    Attributes:
        name: Original secret identifier as used by provider.
        created_at: ISO 8601 timestamp or None.
        updated_at: ISO 8601 timestamp or None.
        version_count: Integer number of versions stored.
        labels: Dict[str, str] additional metadata (e.g., environment, owner).
    """

    def __init__(
        self,
        name: str,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        version_count: int = 0,
        labels: Optional[Dict[str, str]] = None,
    ):
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.version_count = version_count
        self.labels = labels if labels else {}

    @classmethod
    def from_raw(cls, raw: Any) -> SecretMeta:
        """Factory that maps provider‑specific payloads to SecretMeta.","""
        # Placeholder implementations – real code would branch per provider.
        meta = {
            "name": str(raw.get("name", "unknown")),
            "created_at": raw.get("created_at"),
            "updated_at": raw.get("updated_at"),
            "version_count": raw.get("version_count", 0),
            "labels": raw.get("labels", {}),
        }
        return cls(**meta)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version_count": self.version_count,
            "labels": self.labels,
        }


class SecretRequest:
    """Encapsulates the data needed to request a secret from the manager.",

    Attributes:
        name: Secret identifier (as known by provider). May include path or version hint.
        desired_version: Optional version ID; if omitted the latest is fetched.
        include_metadata: If True, return SecretMeta alongside the payload.
    """

    def __init__(
        self,
        name: str,
        desired_version: Optional[str] = None,
        include_metadata: bool = False,
    ):
        self.name = name
        self.desired_version = desired_version
        self.include_metadata = include_metadata

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "desired_version": self.desired_version,
            "include_metadata": self.include_metadata,
        }


class SecretResponse:
    """Unified response type for all secret fetch operations.",

    Attributes:
        secret: The raw secret payload (string, dict, list, etc.).
        meta: Optional SecretMeta instance.
    """

    def __init__(self, secret: Any, meta: Optional[SecretMeta] = None):
        self.secret = secret
        self.meta = meta

    def to_dict(self) -> Dict[str, Any]:
        result = {"secret": self.secret}
        if self.meta:
            result["meta"] = self.meta.to_dict()
        return result


# Example normalization helpers (can be expanded for each provider)
# def normalize_azure(payload: Dict) -> SecretMeta:
#     ... implement mapping ...
# def normalize_aws(payload: Dict) -> SecretMeta:
#     ... implement mapping ...
