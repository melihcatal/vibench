from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional
import json


@dataclass
class SecretReference:
    project_id: str
    secret_id: str
    version: str = "latest"

    def resource_name(self) -> str:
        return f"projects/{self.project_id}/secrets/{self.secret_id}/versions/{self.version}"


@dataclass
class SecretPayload:
    name: str
    value: str
    version: str
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)
    fetched_at: datetime = field(default_factory=datetime.utcnow)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "version": self.version,
            "labels": dict(self.labels),
            "annotations": dict(self.annotations),
            "fetched_at": self.fetched_at.isoformat() + "Z",
        }


@dataclass
class RotationStatus:
    secret_name: str
    version: str
    state: str
    created_time: Optional[str] = None
    destroy_time: Optional[str] = None
    aliases: List[str] = field(default_factory=list)


@dataclass
class SafetyFinding:
    field_name: str
    issue: str
    value: str


UNSAFE_PATTERNS = (
    "password",
    "secret",
    "token",
    "private key",
    "ssh-rsa",
    "api key",
)


def parse_json_secret_value(secret_value: str) -> Dict[str, Any]:
    payload = json.loads(secret_value)
    if not isinstance(payload, dict):
        raise ValueError("Expected top-level JSON object in secret payload")
    return payload



def normalize_labels(labels: Optional[Dict[str, str]]) -> Dict[str, str]:
    return {str(k).strip(): str(v).strip() for k, v in (labels or {}).items() if str(k).strip()}



def detect_unsafe_text(fields: Dict[str, str]) -> List[SafetyFinding]:
    findings: List[SafetyFinding] = []
    for field_name, value in fields.items():
        lowered = value.lower()
        for pattern in UNSAFE_PATTERNS:
            if pattern in lowered:
                findings.append(SafetyFinding(field_name=field_name, issue=f"contains '{pattern}'", value=value))
                break
    return findings



def summarize_rotation(statuses: Iterable[RotationStatus]) -> Dict[str, Any]:
    items = list(statuses)
    active = [s for s in items if s.state.upper() == "ENABLED"]
    disabled = [s for s in items if s.state.upper() != "ENABLED"]
    return {
        "total_versions": len(items),
        "active_versions": len(active),
        "inactive_versions": len(disabled),
        "latest_enabled_version": active[-1].version if active else None,
        "versions": [
            {
                "secret_name": s.secret_name,
                "version": s.version,
                "state": s.state,
                "created_time": s.created_time,
                "destroy_time": s.destroy_time,
                "aliases": list(s.aliases),
            }
            for s in items
        ],
    }
