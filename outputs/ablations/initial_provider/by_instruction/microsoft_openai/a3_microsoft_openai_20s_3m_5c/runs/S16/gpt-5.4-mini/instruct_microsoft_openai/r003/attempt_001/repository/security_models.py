from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_secret_name(name: str) -> str:
    return str(name).strip()


def normalize_stage(stage: Optional[str]) -> Optional[str]:
    if stage is None:
        return None
    value = str(stage).strip()
    return value or None


def normalize_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): normalize_payload(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_payload(v) for v in value]
    if isinstance(value, str):
        return value.strip()
    return value


@dataclass
class SecretRequest:
    name: str
    version: Optional[str] = None
    stage: Optional[str] = None


@dataclass
class SecretResponse:
    name: str
    payload: Dict[str, Any]
    version: Optional[str] = None
    stage: Optional[str] = None
