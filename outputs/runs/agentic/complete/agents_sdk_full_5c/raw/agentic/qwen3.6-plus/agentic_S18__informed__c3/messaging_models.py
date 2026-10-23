"""
Local request, response, and normalization helpers for Pub/Sub Messaging.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class EventMessage:
    """Normalized event message for pub/sub operations."""

    def __init__(
        self,
        event_type: str,
        payload: Dict[str, Any],
        event_id: Optional[str] = None,
        source: Optional[str] = None,
        timestamp: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
    ):
        self.event_id = event_id or str(uuid.uuid4())
        self.event_type = event_type
        self.payload = payload
        self.source = source or "unknown"
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        self.attributes = attributes or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "payload": self.payload,
            "source": self.source,
            "timestamp": self.timestamp,
            "attributes": self.attributes,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventMessage":
        return cls(
            event_type=data["event_type"],
            payload=data.get("payload", {}),
            event_id=data.get("event_id"),
            source=data.get("source"),
            timestamp=data.get("timestamp"),
            attributes=data.get("attributes"),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "EventMessage":
        data = json.loads(json_str)
        return cls.from_dict(data)


class PublishResponse:
    """Normalized response for publish operations."""

    def __init__(
        self,
        success: bool,
        message_ids: List[str],
        error: Optional[str] = None,
        raw_response: Optional[Any] = None,
    ):
        self.success = success
        self.message_ids = message_ids
        self.error = error
        self.raw_response = raw_response
        self.published_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message_ids": self.message_ids,
            "error": self.error,
            "published_at": self.published_at,
        }


class ConsumeResponse:
    """Normalized response for consume operations."""

    def __init__(
        self,
        success: bool,
        message: Optional[EventMessage] = None,
        raw_message: Optional[Any] = None,
        error: Optional[str] = None,
    ):
        self.success = success
        self.message = message
        self.raw_message = raw_message
        self.error = error
        self.consumed_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message.to_dict() if self.message else None,
            "error": self.error,
            "consumed_at": self.consumed_at,
        }


class DeadLetterResponse:
    """Normalized response for dead-letter operations."""

    def __init__(
        self,
        success: bool,
        dead_letter_id: Optional[str] = None,
        original_message_id: Optional[str] = None,
        error: Optional[str] = None,
    ):
        self.success = success
        self.dead_letter_id = dead_letter_id
        self.original_message_id = original_message_id
        self.error = error
        self.dead_lettered_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "dead_letter_id": self.dead_letter_id,
            "original_message_id": self.original_message_id,
            "error": self.error,
            "dead_lettered_at": self.dead_lettered_at,
        }


class ProcessingSummary:
    """Normalized summary of message processing results."""

    def __init__(
        self,
        total_messages: int,
        successful: int,
        failed: int,
        dead_lettered: int,
        summary_text: str,
        details: Optional[List[Dict[str, Any]]] = None,
    ):
        self.total_messages = total_messages
        self.successful = successful
        self.failed = failed
        self.dead_lettered = dead_lettered
        self.summary_text = summary_text
        self.details = details or []
        self.generated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_messages": self.total_messages,
            "successful": self.successful,
            "failed": self.failed,
            "dead_lettered": self.dead_lettered,
            "summary_text": self.summary_text,
            "details": self.details,
            "generated_at": self.generated_at,
        }


class SafetyCheckResult:
    """Normalized result for content safety checks."""

    def __init__(
        self,
        is_safe: bool,
        scores: Dict[str, float],
        categories: List[str],
        flagged_text: Optional[str] = None,
    ):
        self.is_safe = is_safe
        self.scores = scores
        self.categories = categories
        self.flagged_text = flagged_text
        self.checked_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "scores": self.scores,
            "categories": self.categories,
            "flagged_text": self.flagged_text,
            "checked_at": self.checked_at,
        }


class TranslationResult:
    """Normalized result for translation operations."""

    def __init__(
        self,
        original_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
    ):
        self.original_text = original_text
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language
        self.translated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "translated_at": self.translated_at,
        }


class AuditRecord:
    """Normalized audit record for processed messages."""

    def __init__(
        self,
        message_id: str,
        event_type: str,
        status: str,
        processed_at: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.message_id = message_id
        self.event_type = event_type
        self.status = status
        self.processed_at = processed_at
        self.metadata = metadata or {}
        self.record_id = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "message_id": self.message_id,
            "event_type": self.event_type,
            "status": self.status,
            "processed_at": self.processed_at,
            "metadata": self.metadata,
        }


def normalize_payload(payload: Any) -> Dict[str, Any]:
    """Normalize various payload types into a dictionary."""
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"raw_text": payload}
    if isinstance(payload, (list, tuple)):
        return {"items": list(payload)}
    return {"value": payload}


def extract_text_from_payload(payload: Dict[str, Any]) -> str:
    """Extract text content from a payload for safety checks or translation."""
    if "text" in payload:
        return str(payload["text"])
    if "message" in payload:
        return str(payload["message"])
    if "content" in payload:
        return str(payload["content"])
    if "description" in payload:
        return str(payload["description"])
    return json.dumps(payload, default=str)
