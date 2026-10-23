import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_payload(payload: Any) -> bytes:
    if payload is None:
        return b""
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def decode_json_message(raw: Any) -> Dict[str, Any]:
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    if isinstance(raw, str):
        return json.loads(raw)
    return json.loads(str(raw))


@dataclass
class PublishRequest:
    topic: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class PublishBatchRequest:
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
    original_message_id: str
    payload: Dict[str, Any]
    error: str


@dataclass
class ProcessingSummary:
    total: int
    succeeded: int
    failed: int
    notes: List[str] = field(default_factory=list)
