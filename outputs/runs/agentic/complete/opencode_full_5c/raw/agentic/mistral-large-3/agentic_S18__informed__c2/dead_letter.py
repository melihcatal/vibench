from google.cloud import pubsub_v1
import json
import os
from typing import Dict, Any

# Load configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
dead_letter_topic_id = os.getenv("GOOGLE_CLOUD_PUBSUB_DEAD_LETTER_TOPIC_ID")

# Initialize Pub/Sub publisher client for dead-letter topic
publisher = pubsub_v1.PublisherClient()
dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)


def dead_letter(message_data: Dict[str, Any], error_details: str) -> str:
    """
    Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        message_data: The original message data that failed processing.
        error_details: Details about the error that occurred.

    Returns:
        str: The message ID of the published dead-letter message.
    """
    message_data["_error_details"] = error_details
    data = json.dumps(message_data).encode("utf-8")
    future = publisher.publish(dead_letter_topic_path, data)
    return future.result()
