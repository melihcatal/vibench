from __future__ import annotations

from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import decode_message_data, get_pubsub_settings, subscriber_client, subscription_path
from messaging_models import ConsumeResponse


def consume_one_message(timeout: float = 10.0) -> Optional[ConsumeResponse]:
    settings = get_pubsub_settings()
    client = subscriber_client()
    path = subscription_path(settings.project_id, settings.subscription_id)
    response = client.pull(request={"subscription": path, "max_messages": 1, "return_immediately": True}, timeout=timeout)
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    payload = decode_message_data(received.message.data)
    client.acknowledge(request={"subscription": path, "ack_ids": [received.ack_id]})
    return ConsumeResponse(
        ack_id=received.ack_id,
        message_id=received.message.message_id,
        payload=payload,
        attributes=dict(received.message.attributes),
        subscription=path,
    )
