import os
import json
from google.cloud import pubsub_v1

from messaging_client import get_publisher, TOPIC_PATH
from messaging_models import SimpleMessage


def publish_event(message_id: str, payload: dict):
    """
    Publishes a single event to the Google Cloud Pub/Sub topic.

    Args:
        message_id: The unique ID for the message.
        payload: A dictionary representing the message payload.
    """
    publisher = get_publisher()
    message = SimpleMessage(message_id=message_id, payload=payload)
    
    data = json.dumps(message.to_dict()).encode("utf-8")
    
    future = publisher.publish(TOPIC_PATH, data)
    print(f"Published message ID: {future.result()}")
    return future.result()

