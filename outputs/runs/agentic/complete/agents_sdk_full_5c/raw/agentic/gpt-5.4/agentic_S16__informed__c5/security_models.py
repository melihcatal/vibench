from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional
import json


@dataclass
class SecretFetchRequest:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass
class SecretPayload:
    secret_id: str
    version_id: Optional[str]
    value: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "version_id": self.version_id,
            "value": self.value,
            "metadata": self.metadata,
        }


@dataclass
class RotationSummary:
    secret_id: str
    current_version: Optional[str]
    stages: List[str]
    summary: str


def parse_secret_json(secret_string: str) -> Dict[str, Any]:
    parsed = json.loads(secret_string)
    if not isinstance(parsed, dict):
        raise ValueError("Expected JSON object secret payload")
    return parsed


def normalize_secret_response(secret_id: str, response: Mapping[str, Any], value: str) -> SecretPayload:
    return SecretPayload(
        secret_id=secret_id,
        version_id=response.get("VersionId"),
        value=value,
        metadata={
            "ARN": response.get("ARN"),
            "Name": response.get("Name"),
            "VersionStages": response.get("VersionStages", []),
            "CreatedDate": str(response.get("CreatedDate")) if response.get("CreatedDate") is not None else None,
        },
    )
