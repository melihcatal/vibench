from __future__ import annotations

from dataclasses import dataclass
from json import JSONDecodeError
import json
from typing import Any, Dict, Mapping, MutableMapping, Optional


@dataclass(frozen=True)
class SecretRequest:
    secret_name: str
    version: str = "latest"


@dataclass(frozen=True)
class SecretResponse:
    secret_name: str
    version: str
    value: str

    def as_dict(self) -> Dict[str, str]:
        return {"secret_name": self.secret_name, "version": self.version, "value": self.value}


def normalize_secret_value(raw_value: Any) -> str:
    if raw_value is None:
        return ""
    if isinstance(raw_value, bytes):
        return raw_value.decode("utf-8")
    return str(raw_value)


def parse_json_secret_payload(payload: Any) -> Dict[str, Any]:
    text = normalize_secret_value(payload)
    try:
        parsed = json.loads(text)
    except JSONDecodeError as exc:
        raise ValueError("Secret payload is not valid JSON") from exc
    if not isinstance(parsed, MutableMapping):
        raise ValueError("Secret JSON must decode to an object")
    return dict(parsed)


def safe_text_field(value: Optional[str]) -> str:
    return normalize_secret_value(value).strip()
