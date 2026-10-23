from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional
import json


@dataclass(frozen=True)
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass(frozen=True)
class SecretValue:
    secret_id: str
    version_id: Optional[str]
    version_stages: tuple[str, ...]
    secret_string: Optional[str]
    secret_binary: Optional[bytes]
    arn: Optional[str] = None
    created_date: Optional[str] = None


@dataclass(frozen=True)
class RotationSummary:
    secret_id: str
    rotation_enabled: bool
    last_rotated_date: Optional[str]
    next_rotation_date: Optional[str]
    version_ids_to_stages: Dict[str, list[str]]


def normalize_secret_value(secret_id: str, response: Mapping[str, Any]) -> SecretValue:
    binary_value = response.get("SecretBinary")
    if isinstance(binary_value, str):
        binary_value = binary_value.encode("utf-8")
    return SecretValue(
        secret_id=secret_id,
        version_id=response.get("VersionId"),
        version_stages=tuple(response.get("VersionStages") or ()),
        secret_string=response.get("SecretString"),
        secret_binary=binary_value,
        arn=response.get("ARN"),
        created_date=str(response.get("CreatedDate"))
        if response.get("CreatedDate")
        else None,
    )


def parse_secret_json(secret: SecretValue) -> Dict[str, Any]:
    if not secret.secret_string:
        raise ValueError("SecretString is required for JSON parsing")
    parsed = json.loads(secret.secret_string)
    if not isinstance(parsed, dict):
        raise ValueError("Parsed JSON secret must be an object")
    return parsed


def text_from_secret(secret: SecretValue) -> str:
    if secret.secret_string is not None:
        return secret.secret_string
    if secret.secret_binary is not None:
        return secret.secret_binary.decode("utf-8")
    raise ValueError("Secret contained neither SecretString nor SecretBinary")


def normalize_rotation_description(
    secret_id: str, response: Mapping[str, Any]
) -> RotationSummary:
    return RotationSummary(
        secret_id=secret_id,
        rotation_enabled=bool(response.get("RotationEnabled", False)),
        last_rotated_date=str(response.get("LastRotatedDate"))
        if response.get("LastRotatedDate")
        else None,
        next_rotation_date=str(response.get("NextRotationDate"))
        if response.get("NextRotationDate")
        else None,
        version_ids_to_stages={
            k: list(v) for k, v in (response.get("VersionIdsToStages") or {}).items()
        },
    )
