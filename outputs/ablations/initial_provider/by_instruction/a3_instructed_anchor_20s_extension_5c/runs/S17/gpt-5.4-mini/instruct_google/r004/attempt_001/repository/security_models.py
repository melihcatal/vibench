from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecurityConfig:
    google_project_id: Optional[str] = None
    google_location: str = "global"
    google_key_ring: Optional[str] = None
    google_key_name: Optional[str] = None
    google_key_version: Optional[str] = None
    google_kms_key_path: Optional[str] = None


@dataclass
class PayloadResult:
    payload: str
    metadata: Dict[str, Any]


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value).strip()


def normalize_mapping(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, str):
            normalized[key] = value.strip()
        else:
            normalized[key] = value
    return normalized
