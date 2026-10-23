# publish_event.py
# [SAME-SCENARIO]
# Publish a JSON event to Google Cloud Pub/Sub (managed messaging topic)

import os
from google.cloud import pubsub_v1
from .messaging_client import get_publisher_client
from .messaging_models import EventPayload

def publish_event(topic_name: str, payload: dict) -> str:
    """Publish a single JSON event to the specified Pub/Sub topic.
    
    Args:
        topic_name: Name of the Pub/Sub topic (e.g. 'my-topic').
        payload: Dictionary representing the event data.
    Returns:
        The message ID returned by Pub/Sub.
    """
    # Ensure credentials via env variable as required by google-cloud-pubsub
    # GOOGLE_APPLICATION_CREDENTIALS must be set to a service account JSON path.
    publisher = get_publisher_client()
    # Serialize payload to JSON string
    data = EventPayload(data=payload).to_json()
    # Pub/Sub expects bytes
    future = publisher.publish(topic_name, data=data.encode('utf-8'))
    message_id = future.result()
    return message_id