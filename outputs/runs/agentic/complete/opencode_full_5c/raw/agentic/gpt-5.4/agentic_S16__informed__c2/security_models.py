from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass
class SecretValue:
    secret_id: str
    version_id: Optional[str]
    version_stages: List[str]
    secret_string: Optional[str]
    secret_binary: Optional[bytes]
    created_date: Any
    arn: Optional[str]


@dataclass
class RotationSummary:
    secret_id: str
    current_version: Optional[str]
    previous_version: Optional[str]
    stages: Dict[str, List[str]]
    rotation_enabled: bool
    last_rotated_date: Any
    next_rotation_date: Any


def normalize_secret_response(secret_id: str, response: Dict[str, Any]) -> SecretValue:
    secret_binary = response.get("SecretBinary")
    if isinstance(secret_binary, str):
        secret_binary = secret_binary.encode("utf-8")
    return SecretValue(
        secret_id=secret_id,
        version_id=response.get("VersionId"),
        version_stages=list(response.get("VersionStages", [])),
        secret_string=response.get("SecretString"),
        secret_binary=secret_binary,
        created_date=response.get("CreatedDate"),
        arn=response.get("ARN"),
    )


def parse_secret_json(secret: SecretValue) -> Dict[str, Any]:
    import json

    if secret.secret_string:
        return json.loads(secret.secret_string)
    if secret.secret_binary:
        return json.loads(secret.secret_binary.decode("utf-8"))
    return {}


def summarize_rotation(secret_id: str, metadata: Dict[str, Any]) -> RotationSummary:
    version_stage_map = metadata.get("VersionIdsToStages", {})
    current_version = None
    previous_version = None
    normalized: Dict[str, List[str]] = {}
    for version_id, stages in version_stage_map.items():
        normalized[version_id] = list(stages)
        if "AWSCURRENT" in stages:
            current_version = version_id
        if "AWSPREVIOUS" in stages:
            previous_version = version_id
    return RotationSummary(
        secret_id=secret_id,
        current_version=current_version,
        previous_version=previous_version,
        stages=normalized,
        rotation_enabled=bool(metadata.get("RotationEnabled")),
        last_rotated_date=metadata.get("LastRotatedDate"),
        next_rotation_date=metadata.get("NextRotationDate"),
    )
