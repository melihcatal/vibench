from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class NormalizedSecret:
    secret_id: str
    secret_string: Optional[str]
    secret_binary: Optional[bytes]
    version_id: Optional[str]
    version_stages: tuple[str, ...]

    def as_text(self) -> str:
        if self.secret_string is not None:
            return self.secret_string
        if self.secret_binary is not None:
            return self.secret_binary.decode("utf-8", errors="replace")
        return ""


@dataclass(frozen=True)
class SecretFetchResponse:
    provider: str
    secret: NormalizedSecret


@dataclass(frozen=True)
class RotationStatus:
    secret_id: str
    current_version: Optional[str]
    pending_version: Optional[str]
    status: str


@dataclass(frozen=True)
class TextSafetyResult:
    label: str
    unsafe: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class EmbeddingRequest:
    text: str
    model: str


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_lang: str
    target_lang: str


def normalize_secret_value(secret_id: str, payload: Mapping[str, Any]) -> NormalizedSecret:
    version_stages = tuple(payload.get("VersionStages", []) or [])
    secret_binary = payload.get("SecretBinary")
    if isinstance(secret_binary, str):
        secret_binary = secret_binary.encode("utf-8")
    return NormalizedSecret(
        secret_id=secret_id,
        secret_string=payload.get("SecretString"),
        secret_binary=secret_binary,
        version_id=payload.get("VersionId"),
        version_stages=version_stages,
    )


def parse_json_secret(secret_text: str) -> Dict[str, Any]:
    data = json.loads(secret_text)
    if not isinstance(data, dict):
        raise ValueError("Expected JSON object secret")
    return data
