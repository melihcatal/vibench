from __future__ import annotations

from google.cloud import pubsub_v1

from messaging_client import ack_message, pull_one, subscription_path


def consume_event(auto_ack: bool = False) -> dict[str, object] | None:
    provider_client = pubsub_v1.SubscriberClient()
    provider_subscription = subscription_path()
    message = pull_one(auto_ack=auto_ack)
    if message is None:
        return None
    if auto_ack:
        acked = True
    else:
        ack_message(message.ack_id)
        acked = True
    return {
        "provider": "google-cloud-pubsub",
        "subscription": provider_subscription,
        "provider_client": provider_client.__class__.__name__,
        "acknowledged": acked,
        "message": {
            "message_id": message.message_id,
            "payload": message.payload,
            "attributes": message.attributes,
            "published_at": message.published_at,
        },
    }
