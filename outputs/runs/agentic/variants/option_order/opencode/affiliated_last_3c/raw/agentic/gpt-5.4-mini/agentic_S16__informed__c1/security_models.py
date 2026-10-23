from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    secret_name: str
    version_id: Optional[str] = None
    stage: Optional[str] = None


@dataclass
class SecretResponse:
    name: str
    value: Any
    version_id: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_secret_value(value: Any) -> Any:
    if isinstance(value, dict) and "SecretString" in value:
        return value["SecretString"]
    if isinstance(value, dict) and "secretString" in value:
        return value["secretString"]
    return value
