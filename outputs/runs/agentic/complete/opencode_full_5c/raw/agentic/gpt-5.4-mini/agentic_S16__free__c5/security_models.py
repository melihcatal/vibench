import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretPayload:
    secret_id: str
    value: str
    version: str = "latest"


def decode_secret_bytes(raw: bytes) -> str:
    return raw.decode("utf-8")


def parse_json_payload(text: str) -> Dict[str, Any]:
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("expected object secret payload")
    return data


def normalize_staged_version(version: Optional[str]) -> str:
    return version or "latest"
