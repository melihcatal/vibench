from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class EventMessage:
    event: Dict[str, Any]
    message_id: Optional[str] = None
    content_type: str = "application/json"
    session_id: Optional[str] = None
    correlation_id: Optional[str] = None
    label: Optional[str] = None
    to: Optional[str] = None
    reply_to: Optional[str] = None
    time_to_live: Optional[int] = None # in seconds

@dataclass
class ServiceBusConfig:
    connection_string: str
    topic_name: Optional[str] = None
    queue_name: Optional[str] = None
    subscription_name: Optional[str] = None
    dead_letter_queue_name: Optional[str] = None

@dataclass
class ContentSafetyRequest:
    text: str

@dataclass
class ContentSafetyResponse:
    is_safe: bool
    moderation_results: Dict[str, Any]

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class AuditRecord:
    message_id: str
    event_payload: Dict[str, Any]
    processed_at: str
    status: str
    processing_summary: Optional[str] = None
    safety_check_results: Optional[Dict[str, Any]] = None
    translation_results: Optional[Dict[str, Any]] = None
