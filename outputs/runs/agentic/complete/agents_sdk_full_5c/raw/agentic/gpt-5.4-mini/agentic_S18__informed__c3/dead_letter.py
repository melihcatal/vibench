from __future__ import annotations

from typing import Any, Dict

from messaging_client import get_pubsub_settings, publish_json, topic_path
from messaging_models import MessageEnvelope, PublishResponse


def send_to_dead_letter(payload: Dict[str, Any], reason: str, original_message_id: str) -> PublishResponse:
    settings = get_pubsub_settings()
    dead_letter_topic = topic_path(settings.project_id, settings.dead_letter_topic_id)
    envelope = MessageEnvelope(
        event_id=original_message_id,
        event_type="dead-letter",
        source="pubsub-service",
        payload=payload,
        attributes={"reason": reason, "original_message_id": original_message_id, "content_type": "application/json"},
    )
    message_id = publish_json(dead_letter_topic, envelope.to_dict(), envelope.attributes)
    return PublishResponse(message_id=message_id, topic=dead_letter_topic, attributes=envelope.attributes)
