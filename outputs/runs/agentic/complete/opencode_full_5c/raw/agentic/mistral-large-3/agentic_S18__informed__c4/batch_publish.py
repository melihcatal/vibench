from google.cloud import pubsub_v1
import json
import os
from typing import List, Dict, Any
from messaging_client import get_messaging_client


def batch_publish(messages: List[Dict[str, Any]], topic_id: str) -> List[str]:
    """
    Publishes a batch of messages to Google Cloud Pub/Sub topic.

    Args:
        messages: List of dictionaries containing message data.
        topic_id: Google Cloud Pub/Sub topic ID.

    Returns:
        List of message IDs returned by Google Cloud Pub/Sub.
    """
    publisher = get_messaging_client(pubsub_v1.PublisherClient)
    topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id)

    message_ids = []
    for message in messages:
        data = json.dumps(message).encode("utf-8")
        future = publisher.publish(topic_path, data)
        message_ids.append(future.result())

    return message_ids
