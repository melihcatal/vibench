from __future__ import annotations

from google.cloud import pubsub_v1

from messaging_client import get_config, get_subscriber, subscription_path
from messaging_models import ConsumedMessage, MessageResult


def consume_event() -> dict:
    cfg = get_config()
    subscriber: pubsub_v1.SubscriberClient = get_subscriber()
    response = subscriber.pull(subscription=subscription_path(cfg.subscription_id), max_messages=1, timeout=5.0)
    if not response.received_messages:
        return MessageResult(ok=False, provider="google-cloud-pubsub", destination=subscription_path(cfg.subscription_id), details={"reason": "no_messages"}).to_dict()
    received = response.received_messages[0]
    message = ConsumedMessage.from_any(
        {
            "message_id": received.message.message_id,
            "body": {"data": received.message.data.decode("utf-8", errors="replace")},
            "attributes": dict(received.message.attributes),
            "raw_text": received.message.data.decode("utf-8", errors="replace"),
        }
    )
    subscriber.acknowledge(subscription=subscription_path(cfg.subscription_id), ack_ids=[received.ack_id])
    return MessageResult(
        ok=True,
        provider="google-cloud-pubsub",
        destination=subscription_path(cfg.subscription_id),
        message_id=message.message_id,
        details=message.body,
    ).to_dict()
