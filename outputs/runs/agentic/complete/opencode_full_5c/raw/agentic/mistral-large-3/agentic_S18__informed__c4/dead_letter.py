from google.cloud import pubsub_v1
import json
import os
from typing import Dict, Any
from messaging_client import get_messaging_client


def dead_letter(message_data: Dict[str, Any], dead_letter_topic_id: str) -> str:
    """
    Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        message_data: Dictionary containing the failed message data.
        dead_letter_topic_id: Google Cloud Pub/Sub dead-letter topic ID.

    Returns:
        Message ID returned by Google Cloud Pub/Sub.
    """
    publisher = get_messaging_client(pubsub_v1.PublisherClient)
    topic_path = publisher.topic_path(
        os.getenv("GOOGLE_CLOUD_PROJECT"), dead_letter_topic_id
    )

    data = json.dumps(message_data).encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()

    return message_id
