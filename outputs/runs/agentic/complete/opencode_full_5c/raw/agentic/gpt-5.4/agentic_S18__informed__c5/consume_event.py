from __future__ import annotations

from messaging_client import decode_message, subscriber_client, subscription_path


def consume_event(ack: bool = False) -> dict | None:
    client = subscriber_client()
    response = client.pull(
        request={
            "subscription": subscription_path(),
            "max_messages": 1,
        }
    )
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    consumed = decode_message(
        received.message, received.ack_id, getattr(received, "delivery_attempt", None)
    )
    if ack:
        client.acknowledge(
            request={"subscription": subscription_path(), "ack_ids": [received.ack_id]}
        )
    result = consumed.as_dict()
    result["provider"] = "google-cloud-pubsub"
    result["subscription"] = subscription_path()
    return result
