from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Message:
    id: str
    body: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None


@dataclass
class PublishResponse:
    message_id: str


@dataclass
class ConsumeResponse:
    messages: List[Message]


@dataclass
class BatchPublishRequest:
    messages: List[Dict[str, Any]]
    topic_arn: str


@dataclass
class MessageSummary:
    message_id: str
    summary: str


@dataclass
class MessageSafetyResult:
    message_id: str
    is_safe: bool
    details: Dict[str, Any]


@dataclass
class TranslatedPayload:
    message_id: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class AuditRecord:
    message_id: str
    timestamp: str
    status: str
    details: Dict[str, Any]
