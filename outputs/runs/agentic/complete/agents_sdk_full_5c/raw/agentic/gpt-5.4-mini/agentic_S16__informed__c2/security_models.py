from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional
import json


def normalize_secret_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


@dataclass
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    stage: Optional[str] = None
    region: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"secret_id": self.secret_id}
        if self.version_id:
            data["version_id"] = self.version_id
        if self.stage:
            data["stage"] = self.stage
        if self.region:
            data["region"] = self.region
        return data


@dataclass
class SecretResponse:
    secret_id: str
    value: str
    version_id: Optional[str] = None
    metadata: Optional[Mapping[str, Any]] = None

    def normalized(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "value": normalize_secret_text(self.value),
            "version_id": self.version_id,
            "metadata": dict(self.metadata or {}),
        }


@dataclass
class RotationSummary:
    secret_id: str
    current_version: Optional[str]
    previous_version: Optional[str]
    staged_label: Optional[str]
    rotated: bool


@dataclass
class SafetyReport:
    label: str
    note: str
    is_safe: bool
    reasons: list[str]


@dataclass
class EmbeddingRequest:
    text: str
    model: str


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
