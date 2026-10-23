import json
import os

from messaging_client import get_publisher_client, get_project_id, get_topic_path

def publish_event(topic_id: str, event_data: dict):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    publisher = get_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    data = json.dumps(event_data).encode("utf-8")

    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

