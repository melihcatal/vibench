from __future__ import annotations

from google.cloud import pubsub_v1

from messaging_client import get_config, get_publisher, topic_path, to_pubsub_attributes
from messaging_models import MessageEnvelope, MessageResult, normalize_message_payload


def publish_event(payload: dict | str, attributes: dict | None = None) -> dict:
    cfg = get_config()
    envelope = MessageEnvelope(
        event_type="customer.message.published",
        source="publish_event.py",
        attributes=to_pubsub_attributes(attributes),
        payload=normalize_message_payload(payload),
    )
    publisher: pubsub_v1.PublisherClient = get_publisher()
    future = publisher.publish(
        topic_path(cfg.topic_id),
        envelope.to_json().encode("utf-8"),
        **envelope.attributes,
    )
    message_id = future.result()
    return MessageResult(
        ok=True,
        provider="google-cloud-pubsub",
        destination=topic_path(cfg.topic_id),
        message_id=message_id,
        details=envelope.to_dict(),
    ).to_dict()
