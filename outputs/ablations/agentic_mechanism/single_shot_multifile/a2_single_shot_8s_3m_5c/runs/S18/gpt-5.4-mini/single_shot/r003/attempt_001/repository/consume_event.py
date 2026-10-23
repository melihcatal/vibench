import os
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import build_subscriber, resolve_subscription_path
from messaging_models import ReceivedMessage, normalize_received_message


def consume_event() -> Dict[str, Any]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION")
    if not project_id or not subscription_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT and PUBSUB_SUBSCRIPTION are required")

    subscriber = build_subscriber()
    subscription_path = resolve_subscription_path(project_id, subscription_id)
    response = subscriber.pull(subscription=subscription_path, max_messages=1, timeout=10)
    if not response.received_messages:
        return {"subscription": subscription_path, "message": None}

    received = normalize_received_message(response.received_messages[0])
    ack_id = response.received_messages[0].ack_id
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[ack_id])
    return {"subscription": subscription_path, "message": received.to_dict(), "ack_id": ack_id}
