from typing import Any, Dict, List, Literal, Optional, TypedDict

class EventMessage(TypedDict):
    event_id: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]]

class ConsumedMessage(TypedDict):
    event_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str]
    message_id: str
    publish_time: str
    ack_id: str

class BatchPublishResult(TypedDict):
    success: bool
    message_ids: List[str]
    errors: Optional[List[str]]

class SafetyCheckResult(TypedDict):
    is_safe: bool
    categories: List[Dict[str, Any]]
    overall_score: float

class TranslationResult(TypedDict):
    translated_text: str
    source_language: str
    target_language: str

class MessageAuditRecord(TypedDict):
    original_message_id: str
    timestamp: str
    status: Literal['processed', 'dead_lettered', 'failed', 'translated', 'summarized', 'audited']
    details: Dict[str, Any]
