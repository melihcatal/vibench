# batch_publish.py
# [SAME-SCENARIO]
# Publish a batch of JSON events to Google Cloud Pub/Sub.

import os
from google.cloud import pubsub_v1
from .messaging_client import get_publisher_client
from .messaging_models import EventPayload

def batch_publish(topic_name: str, events: list[dict]) -> list[str]:
    """Publish multiple events as separate messages in a single call.

    Args:
        topic_name: Pub/Sub topic name.
        events: List of payload dictionaries.
    Returns:
        List of message IDs corresponding to each published event.
    """
    publisher = get_publisher_client()
    data_list = [EventPayload(data=e).to_json().encode('utf-8') for e in events]
    # Pub/Sub allows up to 1000 messages per publish call.
    future = publisher.publish(topic_name, *data_list)
    message_ids = future.result()
    return message_ids
