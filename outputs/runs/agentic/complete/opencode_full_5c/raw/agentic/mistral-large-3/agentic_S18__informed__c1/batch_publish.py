from google.cloud import pubsub_v1
import json
import os
from typing import List, Dict, Any
from messaging_client import get_publisher_client
from messaging_models import BatchEvent


def batch_publish(topic_id: str, batch_events: List[Dict[str, Any]]) -> List[str]:
    """
    Publishes a batch of messages to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The Google Cloud Pub/Sub topic ID.
        batch_events: A list of dictionaries, each representing an event to publish.

    Returns:
        A list of message IDs for the published messages.
    """
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id)

    batch = publisher.publish(topic_path, messages=[])
    message_ids = []

    for event_data in batch_events:
        event = BatchEvent(data=event_data)
        message = {
            "data": json.dumps(event.data).encode("utf-8"),
            "attributes": event.attributes,
        }
        batch.publish(message)
        message_ids.append(f"pending_{len(message_ids)}")

    results = batch.close()
    return [result for result in results]
