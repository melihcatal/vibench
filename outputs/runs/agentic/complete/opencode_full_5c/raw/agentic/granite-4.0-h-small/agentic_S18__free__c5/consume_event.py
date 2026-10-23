# consume_event.py
"""
Same-scenario scored implementation: consume_event.py
Provides a function to consume one message from a managed Pub/Sub subscription.
"""

from google.cloud import pubsub_v1
from messaging_models import PubSubConfig
import json


def consume_event(config: PubSubConfig) -> dict:
    """Consume one message from a Pub/Sub subscription and return its payload.

    Args:
        config (PubSubConfig): Configuration containing project ID and subscription name.

    Returns:
        dict: The deserialized payload of the consumed message.
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        config.project_id, config.subscription_name
    )
    # Provider identifier in code
    pull_future = subscriber.pull(subscription_path, max_messages=1)
    received_messages = pull_future.result(timeout=10)
    if not received_messages:
        raise RuntimeError("No message received within timeout")
    msg = received_messages[0]
    payload = json.loads(msg.data.decode("utf-8"))
    # Acknowledge the message after processing
    subscriber.acknowledge(subscription_path, [msg.ack_id])
    return payload
