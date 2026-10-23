import base64
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


def _decode_if_needed(value: Optional[str], is_binary: bool) -> Optional[str]:
    if value is None:
        return None
    if not is_binary:
        return value
    return base64.b64decode(value).decode("utf-8")


def normalize_secret_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "SecretString" in payload and payload["SecretString"] is not None:
        return {"value": payload["SecretString"], "source": "SecretString"}
    if "SecretBinary" in payload and payload["SecretBinary"] is not None:
        return {"value": _decode_if_needed(payload["SecretBinary"], True), "source": "SecretBinary"}
    return {"value": None, "source": None}


def parse_json_secret(secret_text: str) -> Dict[str, Any]:
    return json.loads(secret_text)


@dataclass
class SecretRequest:
    secret_id: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class SecretResponse:
    secret_id: str
    value: Optional[str]
    source: Optional[str]
    version_id: Optional[str] = None
