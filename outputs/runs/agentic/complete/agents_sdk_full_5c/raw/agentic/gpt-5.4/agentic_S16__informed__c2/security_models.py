from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional
import json


@dataclass(frozen=True)
class SecretRef:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass(frozen=True)
class SecretPayload:
    secret_id: str
    version_id: Optional[str]
    version_stages: tuple[str, ...]
    value: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "version_id": self.version_id,
            "version_stages": list(self.version_stages),
            "value": self.value,
        }


@dataclass(frozen=True)
class RotationStatus:
    secret_id: str
    current_version: Optional[str]
    previous_version: Optional[str]
    current_labels: tuple[str, ...]
    previous_labels: tuple[str, ...]

    def as_prompt_fragment(self) -> str:
        return (
            f"Secret {self.secret_id}: current_version={self.current_version}, "
            f"previous_version={self.previous_version}, current_labels={list(self.current_labels)}, "
            f"previous_labels={list(self.previous_labels)}"
        )


def normalize_secret_string(response: Mapping[str, Any]) -> str:
    if response.get("SecretString") is not None:
        return str(response["SecretString"])
    if response.get("SecretBinary") is not None:
        raw = response["SecretBinary"]
        if isinstance(raw, bytes):
            return raw.decode("utf-8")
        return str(raw)
    raise ValueError("AWS Secrets Manager response did not include SecretString or SecretBinary")


def parse_json_secret_value(secret_value: str) -> Dict[str, Any]:
    payload = json.loads(secret_value)
    if not isinstance(payload, dict):
        raise ValueError("Expected JSON object secret payload")
    return payload


def redact_secret_text(text: str, keep: int = 4) -> str:
    if len(text) <= keep:
        return "*" * len(text)
    return f"{'*' * (len(text) - keep)}{text[-keep:]}"
