from google.cloud import pubsub_v1
import os
import json
from typing import List, Dict

# Load configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
topic_id = os.getenv("PUBSUB_TOPIC_ID")

# Initialize Pub/Sub publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def batch_publish(messages: List[Dict]) -> List[str]:
    """
    Publishes a batch of messages to a Google Cloud Pub/Sub topic.

    Args:
        messages: List of dictionaries, each containing message data.

    Returns:
        List[str]: List of message IDs for the published messages.
    """
    message_ids = []

    for message in messages:
        # Serialize message data to JSON
        data = json.dumps(message).encode("utf-8")

        # Publish the message
        future = publisher.publish(topic_path, data)
        message_ids.append(future.result())

    return message_ids
