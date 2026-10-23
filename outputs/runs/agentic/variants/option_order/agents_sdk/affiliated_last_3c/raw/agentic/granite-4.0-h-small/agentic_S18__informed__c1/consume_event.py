# consume_event.py
# [SAME-SCENARIO]
# Consume a single JSON event from a Google Cloud Pub/Sub subscription.

import os
from google.cloud import pubsub_v1
from .messaging_client import get_subscriber_client
from .messaging_models import EventMessage

def consume_event(subscription_name: str) -> EventMessage:
    """Pull a single message from the specified Pub/Sub subscription.

    Args:
        subscription_name: Name of the subscription (e.g. 'my-sub').
    Returns:
        An EventMessage instance if a message is received; otherwise None.
    """
    subscriber = get_subscriber_client()
    future = subscriber.pull(subscription_name, max_messages=1, immediate=True)
    response = future.result()
    if not response or not response.received_messages:
        return None
    received = response.received_messages[0]
    # Decode the JSON payload
    payload = received.message.data.decode('utf-8')
    message = EventMessage.parse_json(payload)
    # Acknowledge the message
    subscriber.acknowledge(subscription_name, [received.ack_id])
    return message
