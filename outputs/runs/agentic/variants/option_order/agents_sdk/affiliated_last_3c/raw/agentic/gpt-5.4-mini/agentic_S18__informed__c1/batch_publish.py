from __future__ import annotations

from google.cloud import pubsub_v1

from messaging_client import get_config, get_publisher, topic_path, to_pubsub_attributes
from messaging_models import MessageEnvelope, MessageResult, normalize_message_payload


def batch_publish(messages: list[dict]) -> dict:
    cfg = get_config()
    publisher: pubsub_v1.PublisherClient = get_publisher()
    topic = topic_path(cfg.topic_id)
    futures: list[tuple[str, dict]] = []
    for item in messages:
        payload = normalize_message_payload(item.get("payload", item))
        attrs = to_pubsub_attributes(item.get("attributes"))
        envelope = MessageEnvelope(
            message_id=str(item.get("id") or item.get("message_id") or envelope_id_from_payload(payload)),
            event_type=str(item.get("event_type") or "customer.message.batch"),
            source="batch_publish.py",
            attributes=attrs,
            payload=payload,
        )
        future = publisher.publish(topic, envelope.to_json().encode("utf-8"), **attrs)
        futures.append((future.result(), envelope.to_dict()))
    return MessageResult(ok=True, provider="google-cloud-pubsub", destination=topic, details={"published": futures}).to_dict()


def envelope_id_from_payload(payload: dict) -> str:
    return str(payload.get("id") or payload.get("message_id") or "batch-message")
