from google.cloud import pubsub_v1
import json
import os
from typing import Dict, Any
from messaging_client import get_publisher_client
from messaging_models import Event


def publish_event(
    topic_id: str, event_data: Dict[str, Any], attributes: Dict[str, str] = None
) -> str:
    """
    Publishes a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The Google Cloud Pub/Sub topic ID.
        event_data: The event data to publish as a dictionary.
        attributes: Optional metadata attributes for the message.

    Returns:
        The message ID of the published message.
    """
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id)

    event = Event(data=event_data, attributes=attributes or {})
    future = publisher.publish(
        topic_path, data=json.dumps(event.data).encode("utf-8"), **event.attributes
    )

    return future.result()
