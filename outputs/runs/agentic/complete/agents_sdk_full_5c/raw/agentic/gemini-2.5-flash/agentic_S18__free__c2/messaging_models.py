from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import datetime

@dataclass
class PubSubMessage:
    data: Dict[str, Any]
    message_id: Optional[str] = None
    publish_time: Optional[datetime.datetime] = None
    attributes: Dict[str, str] = field(default_factory=dict)

@dataclass
class EventPayload:
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    source: Optional[str] = None

@dataclass
class ProcessedMessageResult:
    message_id: str
    status: str # e.g., 'SUCCESS', 'FAILED', 'RETRY'
    processed_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    summary: Optional[str] = None
    safety_score: Optional[Dict[str, Any]] = None
    translated_content: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None
