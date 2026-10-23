from __future__ import annotations

from typing import Any

from messaging_client import publisher_client, topic_path
from messaging_models import MessageAttributes, PubSubEvent, PublishResult


PROVIDER = "google-cloud-pubsub"


def publish_event(event_id: str, payload: dict[str, Any], attributes: dict[str, str] | None = None) -> PublishResult:
    client = publisher_client()
    event = PubSubEvent(
        event_id=event_id,
        payload=payload,
        attributes=MessageAttributes.from_dict(attributes),
    )
    future = client.publish(
        topic_path(),
        event.to_json_bytes(),
        **event.attributes.values,
    )
    message_id = future.result(timeout=30)
    return PublishResult(provider=PROVIDER, message_ids=[message_id])
