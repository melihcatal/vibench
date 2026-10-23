from google.cloud import pubsub_v1
import json
import os
from typing import Optional, Dict, Any
from messaging_client import get_subscriber_client
from messaging_models import Event


def consume_event(
    subscription_id: str, timeout: Optional[float] = None
) -> Optional[Event]:
    """
    Consumes one message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: The Google Cloud Pub/Sub subscription ID.
        timeout: Optional timeout in seconds for pulling the message.

    Returns:
        An Event object if a message was received, None otherwise.
    """
    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), subscription_id
    )

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
            "return_immediately": False,
        },
        timeout=timeout,
    )

    if not response.received_messages:
        return None

    message = response.received_messages[0]
    event_data = json.loads(message.message.data.decode("utf-8"))
    event = Event(data=event_data, attributes=message.message.attributes or {})

    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [message.ack_id]}
    )

    return event
