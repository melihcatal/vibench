from google.cloud import pubsub_v1
import json
import os
from typing import List, Dict, Any

# Load configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
topic_id = os.getenv("GOOGLE_CLOUD_PUBSUB_TOPIC_ID")

# Initialize Pub/Sub publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def batch_publish(messages: List[Dict[str, Any]]) -> List[str]:
    """
    Publishes a batch of messages to Google Cloud Pub/Sub topic.

    Args:
        messages: List of dictionaries, each containing "data" and optional "attributes".

    Returns:
        List[str]: List of message IDs for the published messages.
    """
    message_ids = []
    for message in messages:
        data = json.dumps(message["data"]).encode("utf-8")
        attributes = message.get("attributes", {})
        future = publisher.publish(topic_path, data, **attributes)
        message_ids.append(future.result())

    return message_ids
