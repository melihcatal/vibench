import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class Event:
    event_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)

@dataclass
class PublishRequest:
    event: Dict[str, Any]
    topic_id: str
    project_id: str

@dataclass
class PublishResponse:
    message_id: str

@dataclass
class ConsumeRequest:
    subscription_id: str
    project_id: str
    max_messages: int = 1

@dataclass
class Message:
    message_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str]
    ack_id: str

@dataclass
class ConsumeResponse:
    messages: List[Message] = field(default_factory=list)

@dataclass
class DeadLetterRequest:
    message: Message
    dead_letter_topic_id: str
    project_id: str

@dataclass
class BatchPublishRequest:
    events: List[Dict[str, Any]]
    topic_id: str
    project_id: str

@dataclass
class BatchPublishResponse:
    message_ids: List[str] = field(default_factory=list)

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    project_id: str

@dataclass
class TranslationResponse:
    translated_text: str

@dataclass
class SafetyCheckRequest:
    text: str

@dataclass
class SafetyCheckResponse:
    is_unsafe: bool
    scores: Dict[str, float]

@dataclass
class AuditRecord:
    message_id: str
    timestamp: str
    status: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AuditStoreRequest:
    record: AuditRecord
    collection_id: str
    project_id: str

@dataclass
class AuditStoreResponse:
    document_id: str
