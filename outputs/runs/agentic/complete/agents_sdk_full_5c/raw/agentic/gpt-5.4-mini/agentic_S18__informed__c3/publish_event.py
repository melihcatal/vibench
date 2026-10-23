from __future__ import annotations

import os
from typing import Any, Dict

from messaging_client import get_pubsub_settings, publish_json, topic_path
from messaging_models import MessageEnvelope, PublishResponse


def publish_event(payload: Dict[str, Any], event_type: str = "customer.event", source: str = "pubsub-service") -> PublishResponse:
    settings = get_pubsub_settings()
    topic = topic_path(settings.project_id, settings.topic_id)
    envelope = MessageEnvelope(
        event_id=payload.get("event_id", os.urandom(8).hex()),
        event_type=event_type,
        source=source,
        payload=payload,
        attributes={"content_type": "application/json", "event_type": event_type},
    )
    message_id = publish_json(topic, envelope.to_dict(), envelope.attributes)
    return PublishResponse(message_id=message_id, topic=topic, attributes=envelope.attributes)
