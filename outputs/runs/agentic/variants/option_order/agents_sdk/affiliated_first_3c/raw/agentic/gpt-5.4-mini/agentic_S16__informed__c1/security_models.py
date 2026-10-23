from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional


@dataclass(frozen=True)
class SecretRequest:
    secret_id: str
    version: str = "latest"
    project_id: Optional[str] = None


@dataclass(frozen=True)
class SecretPayload:
    secret_id: str
    value: str
    version: str
    provider: str

    def as_json_dict(self) -> Dict[str, Any]:
        return json.loads(self.value)


@dataclass(frozen=True)
class NormalizedSecret:
    name: str
    labels: Dict[str, str]
    notes: str = ""


def normalize_secret_name(value: str) -> str:
    value = value.strip().replace(" ", "-")
    return re.sub(r"[^a-zA-Z0-9_\-]", "", value)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def join_lines(values: Iterable[Any]) -> str:
    return "\n".join(normalize_text(v) for v in values if normalize_text(v))


def to_text_secret(secret_id: str, value: str, version: str, provider: str) -> SecretPayload:
    return SecretPayload(secret_id=secret_id, value=value, version=version, provider=provider)
