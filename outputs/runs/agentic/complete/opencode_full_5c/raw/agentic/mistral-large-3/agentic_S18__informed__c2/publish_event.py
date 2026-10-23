from google.cloud import pubsub_v1
import json
import os
from typing import Dict, Any

# Load configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
topic_id = os.getenv("GOOGLE_CLOUD_PUBSUB_TOPIC_ID")

# Initialize Pub/Sub publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def publish_event(event_data: Dict[str, Any], attributes: Dict[str, str] = None) -> str:
    """
    Publishes a JSON event to Google Cloud Pub/Sub topic.

    Args:
        event_data: Dictionary containing the event payload.
        attributes: Optional dictionary of message attributes.

    Returns:
        str: The message ID of the published message.
    """
    data = json.dumps(event_data).encode("utf-8")
    future = publisher.publish(topic_path, data, **(attributes or {}))
    return future.result()
