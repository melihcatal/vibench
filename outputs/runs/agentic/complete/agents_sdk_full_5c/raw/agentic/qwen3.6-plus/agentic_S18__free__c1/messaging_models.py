"""messaging_models.py - Request, response, and normalization helpers for Pub/Sub Messaging."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PubSubPublishRequest:
    """Request model for publishing a single event to Google Cloud Pub/Sub."""

    topic_id: str
    project_id: str
    event_data: dict
    event_id: str | None = None

    def full_topic_name(self) -> str:
        """Return the fully qualified topic name."""
        return f"projects/{self.project_id}/topics/{self.topic_id}"


@dataclass
class PubSubPublishResponse:
    """Response model for a publish operation."""

    message_id: str | None
    status: str
    topic_name: str | None = None
    error: str | None = None


@dataclass
class PubSubConsumeResponse:
    """Response model for consuming a single message."""

    message_id: str | None
    payload: dict | None
    attributes: dict
    status: str
    error: str | None = None


@dataclass
class PubSubDeadLetterRequest:
    """Request model for sending a message to a dead-letter topic."""

    topic_path: str
    payload: dict
    attributes: dict = field(default_factory=dict)


@dataclass
class PubSubDeadLetterResponse:
    """Response model for a dead-letter operation."""

    dead_letter_message_id: str | None
    original_message_id: str
    status: str
    topic_name: str | None = None
    error: str | None = None


@dataclass
class PubSubMessageEntry:
    """Single message entry for batch publishing."""

    message_id: str
    payload: dict
    attributes: dict = field(default_factory=dict)


@dataclass
class PubSubBatchPublishRequest:
    """Request model for batch publishing to Google Cloud Pub/Sub."""

    topic_path: str
    messages: list[PubSubMessageEntry]

    def message_count(self) -> int:
        return len(self.messages)


@dataclass
class PubSubBatchPublishResponse:
    """Response model for batch publish operation."""

    topic_name: str
    total: int
    published_count: int
    failed_count: int
    results: list[dict] = field(default_factory=list)


def normalize_payload(raw_payload: Any) -> dict:
    """Normalize incoming payload to a dictionary for Pub/Sub publishing.

    Handles dict, string (assumed JSON), and list (wrapped) inputs.
    """
    if isinstance(raw_payload, dict):
        return raw_payload
    if isinstance(raw_payload, str):
        import json
        return json.loads(raw_payload)
    if isinstance(raw_payload, list):
        return {"items": raw_payload}
    return {"value": raw_payload}


def parse_message_attributes(attributes: dict | None) -> dict:
    """Parse and normalize Pub/Sub message attributes."""
    if not attributes:
        return {}
    return {k: str(v) for k, v in attributes.items()}
