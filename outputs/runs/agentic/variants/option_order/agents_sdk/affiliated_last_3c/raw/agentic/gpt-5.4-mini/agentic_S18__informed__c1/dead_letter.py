from __future__ import annotations

from google.cloud import pubsub_v1

from messaging_client import dead_letter_topic_path, get_config, get_publisher, to_pubsub_attributes
from messaging_models import MessageEnvelope, MessageResult, normalize_message_payload


def send_to_dead_letter(payload: dict | str, reason: str, attributes: dict | None = None) -> dict:
    cfg = get_config()
    publisher: pubsub_v1.PublisherClient = get_publisher()
    envelope = MessageEnvelope(
        event_type="customer.message.dead_letter",
        source="dead_letter.py",
        attributes={**to_pubsub_attributes(attributes), "dead_letter_reason": reason},
        payload={"reason": reason, "original": normalize_message_payload(payload)},
    )
    message_id = publisher.publish(dead_letter_topic_path(cfg.dead_letter_topic_id), envelope.to_json().encode("utf-8"), **envelope.attributes).result()
    return MessageResult(ok=True, provider="google-cloud-pubsub", destination=dead_letter_topic_path(cfg.dead_letter_topic_id), message_id=message_id, details=envelope.to_dict()).to_dict()
