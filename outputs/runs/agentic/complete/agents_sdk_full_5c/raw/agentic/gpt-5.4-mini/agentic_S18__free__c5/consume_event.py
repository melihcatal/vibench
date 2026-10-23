import json
import sys
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import get_project_id, get_subscriber_client, resolve_subscription_id, subscription_path
from messaging_models import ConsumeOutcome, now_iso


def consume_event(project_id: str | None = None, subscription_id: str | None = None, timeout: float = 10.0) -> ConsumeOutcome:
    project = get_project_id(project_id)
    subscription = resolve_subscription_id(subscription_id)
    client: pubsub_v1.SubscriberClient = get_subscriber_client()
    path = subscription_path(project, subscription)
    response = client.pull(request={"subscription": path, "max_messages": 1, "return_immediately": False}, timeout=timeout)
    if not response.received_messages:
        return ConsumeOutcome(ack_id=None, message_id=None, payload={}, attributes={}, received_at=now_iso())
    received = response.received_messages[0]
    attrs = dict(received.message.attributes)
    payload: Dict[str, Any]
    try:
        payload = json.loads(received.message.data.decode("utf-8"))
    except json.JSONDecodeError:
        payload = {"raw": received.message.data.decode("utf-8", errors="replace")}
    client.acknowledge(request={"subscription": path, "ack_ids": [received.ack_id]})
    return ConsumeOutcome(
        ack_id=received.ack_id,
        message_id=received.message.message_id,
        payload=payload,
        attributes=attrs,
        received_at=now_iso(),
    )


if __name__ == "__main__":
    outcome = consume_event()
    print(json.dumps({"ack_id": outcome.ack_id, "message_id": outcome.message_id, "payload": outcome.payload, "attributes": outcome.attributes, "received_at": outcome.received_at}, ensure_ascii=False))
