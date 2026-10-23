from google.cloud import pubsub_v1
import json
import os
from typing import Dict, Any
from messaging_client import get_messaging_client
from messaging_models import Event


def publish_event(event_data: Dict[str, Any], topic_id: str) -> str:
    """
    Publishes a JSON event to Google Cloud Pub/Sub topic.

    Args:
        event_data: Dictionary containing event data to publish.
        topic_id: Google Cloud Pub/Sub topic ID.

    Returns:
        Message ID returned by Google Cloud Pub/Sub.
    """
    publisher = get_messaging_client(pubsub_v1.PublisherClient)
    topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id)

    event = Event(**event_data)
    data = json.dumps(event.dict()).encode("utf-8")

    future = publisher.publish(topic_path, data)
    message_id = future.result()

    return message_id
