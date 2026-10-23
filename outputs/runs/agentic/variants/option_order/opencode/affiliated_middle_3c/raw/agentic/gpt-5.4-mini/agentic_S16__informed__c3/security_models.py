import json
from dataclasses import dataclass


@dataclass(frozen=True)
class SecretValue:
    name: str
    value: str


def normalize_secret_text(payload: str) -> str:
    return payload.strip()


def parse_json_secret_text(payload: str):
    return json.loads(payload)
