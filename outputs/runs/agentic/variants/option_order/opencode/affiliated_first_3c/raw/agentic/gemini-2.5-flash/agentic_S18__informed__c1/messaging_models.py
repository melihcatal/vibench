import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PubSubMessage:
    data: bytes
    attributes: Optional[Dict[str, str]] = None
    message_id: Optional[str] = None


@dataclass
class PublishResponse:
    message_ids: List[str]


@dataclass
class ConsumeResponse:
    message: Optional[PubSubMessage] = None
    ack_id: Optional[str] = None


@dataclass
class Event:
    event_id: str
    event_type: str
    payload: Dict[str, Any]

    def to_json(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


@dataclass
class AuditRecord:
    message_id: str
    timestamp: str
    status: str
    payload: Dict[str, Any]
    summary: Optional[str] = None
    safety_scores: Optional[Dict[str, float]] = None
    translated_payload: Optional[Dict[str, Any]] = None
