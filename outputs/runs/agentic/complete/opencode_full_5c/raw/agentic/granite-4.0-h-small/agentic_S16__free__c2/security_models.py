# security_models.py
# [HELPER] Local request, response, and normalization helpers for Secret Management

from typing import Any, Dict


class SecretRequest:
    """Container for a secret retrieval request payload."""

    def __init__(
        self, name: str, version: Optional[int] = None, stage: Optional[str] = None
    ):
        self.name = name
        self.version = version
        self.stage = stage

    def to_dict(self) -> Dict[str, Any]:
        payload = {"name": self.name}
        if self.version is not None:
            payload["version"] = self.version
        if self.stage is not None:
            payload["stage"] = self.stage
        return payload


class SecretResponse:
    """Normalized response envelope for any secret manager."""

    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.value = self._extract_value(raw)

    def _extract_value(self, raw: Dict[str, Any]) -> Any:
        # Attempt to normalise different provider shapes
        if "SecretString" in raw:
            return raw["SecretString"]
        if "value" in raw:
            return raw["value"]
        if "payload" in raw:
            return raw["payload"]
        raise ValueError("Unexpected secret response format")


class SecretAuditNote:
    """Structure for embedding audit commentary."""

    def __init__(self, note: str, severity: str = "info", timestamp: str = None):
        self.note = note
        self.severity = severity
        self.timestamp = timestamp or ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "note": self.note,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }
