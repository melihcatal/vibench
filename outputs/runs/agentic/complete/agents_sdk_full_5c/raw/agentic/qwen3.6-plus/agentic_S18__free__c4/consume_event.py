"""Consume one message from a Google Cloud Pub/Sub subscription.

Uses the google-cloud-pubsub SDK to pull a single message from a managed
subscription with automatic acknowledgement handling.
"""

import os
import json
from typing import Optional, Dict, Any, Tuple

from google.cloud import pubsub_v1


def consume_event(
    subscription_path: Optional[str] = None,
    ack_deadline: int = 60,
    auto_ack: bool = True,
) -> Optional[Dict[str, Any]]:
    """Consume one message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_path: Full subscription path like
            "projects/<project-id>/subscriptions/<sub-name>".
        ack_deadline: Acknowledgement deadline in seconds.
        auto_ack: If True, automatically acknowledge the message after reading.

    Returns:
        Dict with message data or None if no message available.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "pubsub-project-001")
    subscription_name = os.environ.get("PUBSUB_SUBSCRIPTION", "events-subscription")

    if subscription_path is None:
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_name)

    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        timeout=10,
    )

    if not response.received_messages:
        return None

    received = response.received_messages[0]
    message = received.message
    ack_id = received.ack_id

    try:
        payload = json.loads(message.data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = message.data.decode("utf-8", errors="replace")

    attributes = dict(message.attributes)

    if auto_ack:
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": [ack_id]}
        )

    result = {
        "status": "consumed",
        "subscription": subscription_path,
        "message_id": message.message_id,
        "ack_id": ack_id,
        "payload": payload,
        "attributes": attributes,
        "publish_time": str(message.publish_time),
    }

    if auto_ack:
        result["acknowledged"] = True

    return result


def consume_with_nack(
    subscription_path: Optional[str] = None,
    ack_deadline: int = 60,
) -> Optional[Dict[str, Any]]:
    """Consume one message and nack it for redelivery.

    Useful for processing scenarios where the consumer wants to defer
    handling the message.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "pubsub-project-001")
    subscription_name = os.environ.get("PUBSUB_SUBSCRIPTION", "events-subscription")

    if subscription_path is None:
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_name)

    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        timeout=10,
    )

    if not response.received_messages:
        return None

    received = response.received_messages[0]
    message = received.message
    ack_id = received.ack_id

    try:
        payload = json.loads(message.data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = message.data.decode("utf-8", errors="replace")

    # Nack the message so it can be redelivered
    subscriber.modify_ack_deadline(
        request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
            "ack_deadline_seconds": 0,
        }
    )

    return {
        "status": "consumed_nacked",
        "subscription": subscription_path,
        "message_id": message.message_id,
        "payload": payload,
        "attributes": dict(message.attributes),
        "redelivered": True,
    }


if __name__ == "__main__":
    result = consume_event()
    if result:
        print(json.dumps(result, indent=2, default=str))
    else:
        print("No messages available.")
