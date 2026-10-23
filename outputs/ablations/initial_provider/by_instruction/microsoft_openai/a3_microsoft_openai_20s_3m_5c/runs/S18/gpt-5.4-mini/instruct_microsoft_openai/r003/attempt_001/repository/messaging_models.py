import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PublishRequest:
    body: Dict[str, Any]
    message_id: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None


@dataclass
class PublishResult:
    message_id: str
    status: str


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        return json.loads(payload)
    return {"value": payload}


def normalize_batch(items: List[Any]) -> List[Dict[str, Any]]:
    return [normalize_payload(item) for item in items]
