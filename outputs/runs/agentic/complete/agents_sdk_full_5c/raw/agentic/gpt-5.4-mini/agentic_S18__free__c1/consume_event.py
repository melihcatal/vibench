from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import load_config, subscriber_client, subscription_path
from messaging_models import ProcessedMessage, normalize_attributes, normalize_payload


def consume_event(ack: bool = True) -> Optional[ProcessedMessage]:
    sub_path = subscription_path()
    response = subscriber_client().pull(subscription=sub_path, max_messages=1, timeout=10)
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    data = received.message.data.decode("utf-8") if received.message.data else "{}"
    payload = normalize_payload(json.loads(data))
    attrs = normalize_attributes(received.message.attributes)
    processed = ProcessedMessage(
        message_id=received.message.message_id,
        ack_id=received.ack_id,
        payload=payload,
        attributes=attrs,
        received_at=datetime.now(timezone.utc).isoformat(),
    )
    if ack:
        subscriber_client().acknowledge(subscription=sub_path, ack_ids=[received.ack_id])
    return processed


if __name__ == "__main__":
    consume_event()
