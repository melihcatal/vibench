import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretPayload:
    name: str
    data: str


def decode_bytes(payload: bytes) -> str:
    return payload.decode("utf-8")


def parse_json_secret(raw: str) -> Dict[str, Any]:
    return json.loads(raw)


def normalize_version(name: str, payload: bytes, etag: Optional[str] = None) -> SecretPayload:
    return SecretPayload(name=name, data=decode_bytes(payload))


def safe_text(value: str) -> str:
    return " ".join(value.split())
