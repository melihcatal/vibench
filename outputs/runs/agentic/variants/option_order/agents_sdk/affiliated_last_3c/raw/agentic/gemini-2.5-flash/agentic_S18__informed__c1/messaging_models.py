import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class EventMessage:
    message_id: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def to_json(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")

@dataclass
class PublishResponse:
    message_id: str

@dataclass
class ConsumeResponse:
    message_id: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
    ack_id: Optional[str] = None

@dataclass
class BatchPublishRequest:
    messages: List[EventMessage]
    
@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    timestamp: str
    status: str
    summary: Optional[str] = None
    safety_scores: Optional[Dict[str, Any]] = None
    translated_payload: Optional[Dict[str, Any]] = None
    original_payload: Optional[Dict[str, Any]] = None
