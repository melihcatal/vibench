import dataclasses
import typing as t


@dataclasses.dataclass
class PublishRequest:
    """Payload for publishing an event."""

    topic: str
    event: dict


@dataclasses.dataclass
class ConsumeResponse:
    """Payload returned after consuming a message."""

    message_id: str
    payload: dict


@dataclasses.dataclass
class DeadLetterRequest:
    """Payload for moving a message to a dead‑letter destination."""

    source_topic: str
    dead_letter_topic: str
    message_id: str
    payload: dict


@dataclass
class BatchPublishRequest:
    """Batch publish container."""

    topic: str
    messages: t.List[dict]


@dataclass
class MessageSummary:
    """Summary produced by message_summary."""

    processed_count: int
    failed_count: int
    dead_letter_count: int


@dataclass
class MessageSafetyResult:
    """Safety check result."""

    safe: bool
    warnings: t.List[str]


@dataclass
class TranslatedText:
    target: str
    translated: str


@dataclass
class AuditRecord:
    timestamp: str
    message_id: str
    payload: dict
    outcome: str  # e.g., 'processed', 'dlq', 'failed'
