from __future__ import annotations

from typing import Any

from messaging_client import dead_letter_topic_path, publisher_client
from messaging_models import MessageAttributes, PubSubEvent, PublishResult


PROVIDER = "google-cloud-pubsub"


def send_to_dead_letter(
    original_message_id: str,
    failed_payload: dict[str, Any],
    reason: str,
    attributes: dict[str, str] | None = None,
) -> PublishResult:
    client = publisher_client()
    merged_attributes = {"dead_letter_reason": reason, "original_message_id": original_message_id}
    if attributes:
        merged_attributes.update({str(k): str(v) for k, v in attributes.items()})

    event = PubSubEvent(
        event_id=f"dlq-{original_message_id}",
        payload=failed_payload,
        attributes=MessageAttributes.from_dict(merged_attributes),
    )
    future = client.publish(dead_letter_topic_path(), event.to_json_bytes(), **event.attributes.values)
    message_id = future.result(timeout=30)
    return PublishResult(provider=PROVIDER, message_ids=[message_id])
