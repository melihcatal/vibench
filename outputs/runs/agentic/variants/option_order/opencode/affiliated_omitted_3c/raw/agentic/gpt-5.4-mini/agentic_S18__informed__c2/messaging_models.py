import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_message_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        text = payload.strip()
        if not text:
            return {}
        return json.loads(text)
    return {"value": payload}


@dataclass
class PublishRequest:
    topic: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class BatchPublishRequest:
    topic: str
    messages: List[Dict[str, Any]]


@dataclass
class ConsumeResponse:
    message_id: Optional[str]
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class DeadLetterRequest:
    destination: str
    original_message_id: Optional[str]
    payload: Dict[str, Any]
    reason: str


@dataclass
class ProcessSummary:
    processed: int
    succeeded: int
    failed: int
    details: Dict[str, Any] = field(default_factory=dict)
