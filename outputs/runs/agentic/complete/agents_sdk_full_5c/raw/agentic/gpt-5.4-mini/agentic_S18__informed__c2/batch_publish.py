from __future__ import annotations

from messaging_client import AzureServiceBusMessagingClient
from messaging_models import MessageEnvelope, normalize_payload


def batch_publish(messages: list[dict]):
    client = AzureServiceBusMessagingClient()
    envelopes = [
        MessageEnvelope(
            event_type=str(item.get("event_type", "message.batch")),
            payload=normalize_payload(item.get("payload", item)),
            attributes={str(k): str(v) for k, v in item.get("attributes", {}).items()},
        )
        for item in messages
    ]
    return client.publish_batch(envelopes)
