import base64
import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_secret_name(name: str) -> str:
    return name.strip().replace(" ", "-").lower()


def normalize_stage(stage: Optional[str]) -> str:
    return (stage or "AWSCURRENT").strip().upper()


def decode_secret_payload(payload: Any) -> Any:
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except Exception:
            try:
                return base64.b64decode(payload).decode("utf-8")
            except Exception:
                return payload
    return payload


@dataclass
class SecretRequest:
    secret_id: str
    stage: str = "AWSCURRENT"


@dataclass
class SecretResponse:
    secret_id: str
    stage: str
    value: Any


def response_dict(secret_id: str, stage: str, value: Any) -> Dict[str, Any]:
    return {"secret_id": secret_id, "stage": stage, "value": value}
