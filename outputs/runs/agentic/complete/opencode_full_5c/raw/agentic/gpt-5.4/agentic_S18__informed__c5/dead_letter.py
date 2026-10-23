from __future__ import annotations

from typing import Any

from messaging_client import dead_letter_topic_path, publisher_client
from messaging_models import normalize_attributes, normalize_payload


def send_to_dead_letter(
    payload: dict[str, Any], reason: str, attributes: dict[str, Any] | None = None
) -> dict[str, str]:
    client = publisher_client()
    message_attributes = normalize_attributes(attributes)
    message_attributes["dead_letter_reason"] = reason
    future = client.publish(
        dead_letter_topic_path(), normalize_payload(payload), **message_attributes
    )
    return {
        "message_id": future.result(),
        "dead_letter_topic": dead_letter_topic_path(),
        "provider": "google-cloud-pubsub",
    }
