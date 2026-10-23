import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


@dataclass
class DeadLetterResult:
    topic_path: str
    message_id: Optional[str]
    attributes: Dict[str, str]


def _publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def _topic_path(project_id: str, dead_letter_topic: str) -> str:
    return _publisher().topic_path(project_id, dead_letter_topic)


def send_failed_message(payload: bytes, project_id: Optional[str] = None, dead_letter_topic: Optional[str] = None, original_message_id: Optional[str] = None, error_reason: Optional[str] = None, source_subscription: Optional[str] = None, extra_attributes: Optional[Dict[str, str]] = None) -> DeadLetterResult:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    dead_letter_topic = dead_letter_topic or os.environ.get("PUBSUB_DEAD_LETTER_TOPIC")
    if not project_id:
        raise ValueError("project_id is required")
    if not dead_letter_topic:
        raise ValueError("dead_letter_topic is required")

    attributes: Dict[str, str] = {
        "destination": "dead-letter",
        "provider": "google-pubsub",
    }
    if original_message_id:
        attributes["original_message_id"] = original_message_id
    if error_reason:
        attributes["error_reason"] = error_reason
    if source_subscription:
        attributes["source_subscription"] = source_subscription
    if extra_attributes:
        attributes.update({str(k): str(v) for k, v in extra_attributes.items()})

    publisher = _publisher()
    topic_path = _topic_path(project_id, dead_letter_topic)
    future = publisher.publish(topic_path, payload, **attributes)
    message_id = future.result()
    return DeadLetterResult(topic_path=topic_path, message_id=message_id, attributes=attributes)


def handle_failure(message: Any, project_id: Optional[str] = None, dead_letter_topic: Optional[str] = None, error_reason: Optional[str] = None, source_subscription: Optional[str] = None) -> DeadLetterResult:
    data = getattr(message, "data", None)
    if data is None:
        data = str(message).encode("utf-8")
    attributes = dict(getattr(message, "attributes", {}) or {})
    original_message_id = getattr(message, "message_id", None)
    return send_failed_message(
        payload=data,
        project_id=project_id,
        dead_letter_topic=dead_letter_topic,
        original_message_id=original_message_id,
        error_reason=error_reason,
        source_subscription=source_subscription,
        extra_attributes=attributes,
    )
