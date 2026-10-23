from typing import Literal, TypedDict


class EventMessage(TypedDict):
    event_id: str
    event_type: str
    timestamp: str
    payload: dict


class MessageSummary(TypedDict):
    summary_text: str
    keywords: list[str]


class SafetyCheckResult(TypedDict):
    is_safe: bool
    details: str


class TranslatedPayload(TypedDict):
    translated_text: str
    source_language: str
    target_language: str


class AuditRecord(TypedDict):
    record_id: str
    original_message_id: str
    timestamp: str
    status: Literal["processed", "failed", "dead_lettered"]
    processing_details: dict
