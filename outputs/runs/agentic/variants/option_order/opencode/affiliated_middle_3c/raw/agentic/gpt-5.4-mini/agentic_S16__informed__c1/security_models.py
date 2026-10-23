import json
from dataclasses import dataclass


@dataclass(frozen=True)
class SecretRequest:
    secret_name: str
    version_stage: str | None = None


def ensure_mapping(value: str) -> dict:
    data = json.loads(value)
    if not isinstance(data, dict):
        raise ValueError("secret is not a JSON object")
    return data


def parse_json_secret_value(value: str) -> dict:
    return ensure_mapping(value)
