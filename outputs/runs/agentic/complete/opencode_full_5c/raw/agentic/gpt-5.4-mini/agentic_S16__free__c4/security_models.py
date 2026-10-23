import json
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SecretPayload:
    value: str


def decode_bytes(payload: bytes) -> str:
    return payload.decode("utf-8")


def parse_json(value: str) -> Dict[str, Any]:
    return json.loads(value)


def normalize_text(value: str) -> str:
    return value.strip()
