import base64
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        return {"text": payload}
    return {"value": payload}


def encode_json_bytes(data: Dict[str, Any]) -> str:
    import json
    return base64.b64encode(json.dumps(data, separators=(",", ":")).encode("utf-8")).decode("ascii")


@dataclass
class PublishRequest:
    topic: str
    event: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class PublishResponse:
    message_id: str
    topic: str


@dataclass
class BatchPublishRequest:
    topic: str
    messages: List[Dict[str, Any]]


@dataclass
class ConsumeResponse:
    ack_id: Optional[str]
    message_id: Optional[str]
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class DeadLetterRequest:
    destination: str
    original_message: Dict[str, Any]
    reason: str


@dataclass
class ProcessingSummary:
    processed: int
    failed: int
    details: List[Dict[str, Any]] = field(default_factory=list)
