from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional
import json


@dataclass(frozen=True)
class SecretRequest:
    secret_name: str
    version: Optional[str] = None
    stage: Optional[str] = None


@dataclass(frozen=True)
class SecretResponse:
    secret_name: str
    value: str
    version: Optional[str] = None
    stage: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


def normalize_secret_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (bytes, bytearray)):
        return value.decode("utf-8")
    if isinstance(value, Mapping):
        return json.dumps(dict(value), sort_keys=True, separators=(",", ":"))
    if isinstance(value, (list, tuple)):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def normalize_secret_response(payload: Mapping[str, Any]) -> SecretResponse:
    secret_name = str(payload.get("secret_name", payload.get("name", "")))
    value = normalize_secret_value(payload.get("value", payload.get("secret_value", "")))
    version = payload.get("version")
    stage = payload.get("stage", payload.get("version_stage"))
    metadata = payload.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        metadata = dict(metadata)
    return SecretResponse(
        secret_name=secret_name,
        value=value,
        version=None if version is None else str(version),
        stage=None if stage is None else str(stage),
        metadata=metadata,
    )


def normalize_secret_request(secret_name: str, version: Optional[str] = None, stage: Optional[str] = None) -> SecretRequest:
    return SecretRequest(secret_name=str(secret_name), version=None if version is None else str(version), stage=None if stage is None else str(stage))
