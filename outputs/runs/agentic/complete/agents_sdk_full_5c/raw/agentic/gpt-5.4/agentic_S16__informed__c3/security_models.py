from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json


@dataclass
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass
class SecretPayload:
    secret_id: str
    name: str
    version_id: Optional[str]
    version_stages: List[str] = field(default_factory=list)
    secret_string: Optional[str] = None
    secret_binary: Optional[bytes] = None

    def text(self) -> str:
        if self.secret_string is not None:
            return self.secret_string
        if self.secret_binary is not None:
            return self.secret_binary.decode("utf-8")
        return ""

    def json_value(self) -> Dict[str, Any]:
        return json.loads(self.text())


@dataclass
class RotationSummary:
    secret_id: str
    rotation_enabled: bool
    last_rotated_date: Optional[str]
    next_rotation_date: Optional[str]
    version_ids_to_stages: Dict[str, List[str]]


def normalize_secret_value(response: Dict[str, Any], secret_id: str) -> SecretPayload:
    return SecretPayload(
        secret_id=secret_id,
        name=response.get("Name", secret_id),
        version_id=response.get("VersionId"),
        version_stages=response.get("VersionStages", []) or [],
        secret_string=response.get("SecretString"),
        secret_binary=response.get("SecretBinary"),
    )


def normalize_rotation_metadata(response: Dict[str, Any], secret_id: str) -> RotationSummary:
    return RotationSummary(
        secret_id=secret_id,
        rotation_enabled=bool(response.get("RotationEnabled", False)),
        last_rotated_date=response.get("LastRotatedDate").isoformat() if response.get("LastRotatedDate") else None,
        next_rotation_date=response.get("NextRotationDate").isoformat() if response.get("NextRotationDate") else None,
        version_ids_to_stages=response.get("VersionIdsToStages", {}) or {},
    )
