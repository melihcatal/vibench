import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SecretRequest:
    secret_id: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class SecretResponse:
    secret_id: str
    secret_string: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None


def normalize_secret_payload(secret_string: str) -> Dict[str, Any]:
    if not secret_string:
        return {}
    try:
        parsed = json.loads(secret_string)
        return parsed if isinstance(parsed, dict) else {"value": parsed}
    except json.JSONDecodeError:
        return {"value": secret_string}
