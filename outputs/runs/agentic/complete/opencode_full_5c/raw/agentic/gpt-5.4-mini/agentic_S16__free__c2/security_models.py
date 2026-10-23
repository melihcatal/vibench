import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_secret_name(name: str) -> str:
    return name.strip().replace(" ", "-")


def normalize_stage(stage: Optional[str]) -> str:
    return (stage or "latest").strip().upper()


def extract_secret_text(response: Dict[str, Any]) -> str:
    if "payload" in response and isinstance(response["payload"], dict):
        data = response["payload"].get("data")
        if isinstance(data, str):
            return data
    return json.dumps(response, sort_keys=True)


@dataclass
class SecretFetchRequest:
    secret_id: str
    version: str = "latest"


@dataclass
class SecretFetchResponse:
    secret_id: str
    version: str
    value: Any


@dataclass
class SecretRotationRequest:
    secret_id: str
    stage: str = "latest"


@dataclass
class SecretRotationSummary:
    secret_id: str
    version: str
    state: str
