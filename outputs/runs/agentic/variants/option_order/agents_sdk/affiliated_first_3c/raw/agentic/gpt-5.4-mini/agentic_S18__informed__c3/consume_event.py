from __future__ import annotations

import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import subscription_path
from messaging_models import ConsumeResponse


def consume_one(subscription: str | None = None, timeout: float = 5.0) -> ConsumeResponse:
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(request={"subscription": subscription_path(subscription), "max_messages": 1}, timeout=timeout)
    if not response.received_messages:
        return ConsumeResponse(message_id=None, payload="", attributes={})
    msg = response.received_messages[0]
    data = msg.message.data.decode("utf-8")
    try:
        payload = json.dumps(json.loads(data), ensure_ascii=False)
    except Exception:
        payload = data
    return ConsumeResponse(
        message_id=msg.message.message_id,
        payload=payload,
        attributes=dict(msg.message.attributes),
        ack_id=msg.ack_id,
    )
