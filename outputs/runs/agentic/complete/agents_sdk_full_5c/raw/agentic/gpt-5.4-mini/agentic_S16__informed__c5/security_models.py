from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional
import json


@dataclass(frozen=True)
class SecretRequest:
    secret_name: str
    version_id: Optional[str] = None
    stage: Optional[str] = None


@dataclass(frozen=True)
class SecretResponse:
    secret_name: str
    raw_value: str
    parsed: Optional[Any] = None
    metadata: Optional[Mapping[str, Any]] = None


def normalize_secret_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def maybe_parse_json_secret(secret_text: str) -> Any:
    try:
        return json.loads(secret_text)
    except Exception:
        return secret_text


def response_to_dict(response: SecretResponse) -> Dict[str, Any]:
    return {
        "secret_name": response.secret_name,
        "raw_value": response.raw_value,
        "parsed": response.parsed,
        "metadata": dict(response.metadata or {}),
    }
