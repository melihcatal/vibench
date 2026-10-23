from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional
import json


@dataclass
class SecretRequest:
    project_id: str
    secret_id: str
    version_id: str = "latest"

    @property
    def resource_name(self) -> str:
        return f"projects/{self.project_id}/secrets/{self.secret_id}/versions/{self.version_id}"


@dataclass
class SecretPayload:
    resource_name: str
    text: str
    data: bytes

    def json(self) -> Dict[str, Any]:
        return json.loads(self.text)


@dataclass
class RotationSummary:
    secret_name: str
    version_name: str
    state: str
    labels: Dict[str, str]
    notes: str


def normalize_labels(labels: Optional[Mapping[str, str]]) -> Dict[str, str]:
    if not labels:
        return {}
    return {str(k).strip().lower(): str(v).strip() for k, v in labels.items()}


def decode_secret_payload(resource_name: str, data: bytes) -> SecretPayload:
    text = data.decode("utf-8")
    return SecretPayload(resource_name=resource_name, text=text, data=data)


def safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
