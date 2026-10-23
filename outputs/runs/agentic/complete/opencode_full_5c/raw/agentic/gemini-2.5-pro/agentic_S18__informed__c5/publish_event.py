import json
import os
from google.cloud import pubsub_v1

from messaging_client import get_publisher_client, get_project_id, TOPIC_ID
from messaging_models import EventPayload


def publish_event(payload: EventPayload):
    """Publishes a single event to a Google Cloud Pub/Sub topic."""
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GCP project ID not set.")

    publisher = get_publisher_client()
    topic_path = publisher.topic_path(project_id, TOPIC_ID)

    data = json.dumps(payload).encode("utf-8")

    future = publisher.publish(topic_path, data)
    return future.result()
