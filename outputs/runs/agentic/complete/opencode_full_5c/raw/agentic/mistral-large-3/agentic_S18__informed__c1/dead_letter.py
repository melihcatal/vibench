from google.cloud import pubsub_v1
import json
import os
from typing import Dict, Any
from messaging_client import get_publisher_client
from messaging_models import Event


def dead_letter(
    topic_id: str, event_data: Dict[str, Any], attributes: Dict[str, str] = None
) -> str:
    """
    Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        topic_id: The Google Cloud Pub/Sub dead-letter topic ID.
        event_data: The failed event data to publish as a dictionary.
        attributes: Optional metadata attributes for the message.

    Returns:
        The message ID of the published message.
    """
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id)

    event = Event(data=event_data, attributes=attributes or {})
    event.attributes["dead_letter_reason"] = event.attributes.get(
        "dead_letter_reason", "unknown"
    )

    future = publisher.publish(
        topic_path, data=json.dumps(event.data).encode("utf-8"), **event.attributes
    )

    return future.result()
