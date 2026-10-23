import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretFetchRequest:
    secret_name: str
    version: str = "latest"


@dataclass
class SecretVersionRequest:
    secret_name: str
    version: str = "latest"
    stage: str = "CURRENT"


@dataclass
class SecretValue:
    secret_name: str
    version: str
    value: str
    normalized: Optional[Any] = None


def normalize_secret_payload(payload: str):
    return payload.strip()


def normalize_json_secret(payload: str):
    return json.loads(payload)
