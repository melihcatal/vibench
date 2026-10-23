from __future__ import annotations

import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import load_config, subscriber_client, subscription_path
from messaging_models import ConsumeResult, normalize_attributes


def consume_one_message(project_id: str | None = None, timeout: float = 10.0) -> ConsumeResult:
    config = load_config(project_id)
    client = subscriber_client()
    response = client.pull(
        request={"subscription": subscription_path(config), "max_messages": 1},
        timeout=timeout,
    )
    if not response.received_messages:
        raise RuntimeError("No message available")
    received = response.received_messages[0]
    payload = json.loads(received.message.data.decode("utf-8"))
    client.acknowledge(request={"subscription": subscription_path(config), "ack_ids": [received.ack_id]})
    return ConsumeResult(
        ack_id=received.ack_id,
        message_id=payload.get("message_id", received.message.message_id),
        payload=payload.get("payload", payload),
        attributes=normalize_attributes(payload.get("attributes", {})),
    )
