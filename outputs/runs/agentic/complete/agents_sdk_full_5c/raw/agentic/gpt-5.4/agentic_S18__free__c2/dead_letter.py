from __future__ import annotations

from typing import Any, Mapping, Optional

from messaging_client import dead_letter_topic_path, publisher_client
from messaging_models import EventMessage


def send_to_dead_letter(
    failed_payload: Mapping[str, Any],
    *,
    error_message: str,
    original_message_id: Optional[str] = None,
    dead_letter_topic_id: Optional[str] = None,
    project_id: Optional[str] = None,
) -> str:
    client = publisher_client()
    attributes = {
        "dead_letter_reason": error_message,
        "original_message_id": original_message_id or "unknown",
        "source": "google-pubsub",
    }
    event = EventMessage.from_mapping(failed_payload, attributes=attributes)
    future = client.publish(
        dead_letter_topic_path(topic_id=dead_letter_topic_id, project_id=project_id),
        event.to_json_bytes(),
        **event.attributes,
    )
    return future.result()
