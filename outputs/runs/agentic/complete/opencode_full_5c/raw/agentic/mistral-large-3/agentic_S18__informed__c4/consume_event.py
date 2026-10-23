from google.cloud import pubsub_v1
import json
import os
from typing import Dict, Any, Optional
from messaging_client import get_messaging_client


def consume_event(
    subscription_id: str, timeout: Optional[float] = None
) -> Optional[Dict[str, Any]]:
    """
    Consumes one message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: Google Cloud Pub/Sub subscription ID.
        timeout: Optional timeout in seconds for pulling the message.

    Returns:
        Dictionary containing the message data, or None if no message was received.
    """
    subscriber = get_messaging_client(pubsub_v1.SubscriberClient)
    subscription_path = subscriber.subscription_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), subscription_id
    )

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
            "return_immediately": False if timeout else True,
        },
        timeout=timeout,
    )

    if not response.received_messages:
        return None

    message = response.received_messages[0]
    data = json.loads(message.message.data.decode("utf-8"))

    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [message.ack_id],
        }
    )

    return data
