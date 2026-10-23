from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List


@dataclass
class PubsubMessage:
    data: Dict[str, Any]
    message_id: Optional[str] = None
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class PublishRequest:
    message: PubsubMessage


@dataclass
class PublishResponse:
    message_id: str


@dataclass
class ConsumeResponse:
    message: PubsubMessage
    ack_id: str


@dataclass
class BatchPublishRequest:
    messages: List[PubsubMessage]


@dataclass
class BatchPublishResponse:
    message_ids: List[str]


@dataclass
class AuditRecord:
    message_id: str
    timestamp: str
    event_type: str
    payload_summary: str
    status: str
