from __future__ import annotations

from typing import Any

from messaging_client import publisher_client, topic_path
from messaging_models import MessageEvent, normalize_attributes


def publish_event(
    payload: dict[str, Any],
    attributes: dict[str, Any] | None = None,
    ordering_key: str | None = None,
) -> dict[str, str]:
    event = MessageEvent(
        payload=payload,
        attributes=normalize_attributes(attributes),
        ordering_key=ordering_key,
    )
    client = publisher_client()
    future = client.publish(
        topic_path(),
        event.to_pubsub_payload(),
        ordering_key=event.ordering_key or "",
        **event.attributes,
    )
    return {
        "message_id": future.result(),
        "topic": topic_path(),
        "provider": "google-cloud-pubsub",
    }
