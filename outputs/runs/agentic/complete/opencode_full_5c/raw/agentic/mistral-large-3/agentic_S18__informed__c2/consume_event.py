from google.cloud import pubsub_v1
import json
import os
from typing import Dict, Any, Optional

# Load configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
subscription_id = os.getenv("GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION_ID")

# Initialize Pub/Sub subscriber client
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def consume_event() -> Optional[Dict[str, Any]]:
    """
    Consumes one message from Google Cloud Pub/Sub subscription.

    Returns:
        Optional[Dict[str, Any]]: The message data as a dictionary, or None if no message was received.
    """
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )

    if not response.received_messages:
        return None

    message = response.received_messages[0]
    data = json.loads(message.message.data.decode("utf-8"))

    # Acknowledge the message
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [message.ack_id]}
    )

    return data
