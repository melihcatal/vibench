import json
from typing import List
from google.cloud import pubsub_v1

from messaging_client import get_publisher_client, get_project_id, TOPIC_ID
from messaging_models import EventPayload


def batch_publish(events: List[EventPayload]):
    """Publishes a batch of messages to a Google Cloud Pub/Sub topic."""
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GCP project ID not set.")

    publisher = get_publisher_client()
    topic_path = publisher.topic_path(project_id, TOPIC_ID)

    publish_futures = []
    for event in events:
        data = json.dumps(event).encode("utf-8")
        future = publisher.publish(
            topic_path, data, message_id=event.get("message_id", "")
        )
        publish_futures.append(future)

    results = [future.result() for future in publish_futures]
    return results
