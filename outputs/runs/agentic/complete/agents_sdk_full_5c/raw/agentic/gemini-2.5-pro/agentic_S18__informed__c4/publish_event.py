import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_project_id, get_topic_path
from messaging_models import Event

def publish_event(event: Event):
    """Publishes a single event to a Google Cloud Pub/Sub topic."""
    project_id = get_project_id()
    topic_id = os.getenv("GCP_PUBSUB_TOPIC_ID", "my-topic")

    publisher = get_publisher_client()
    topic_path = get_topic_path(publisher, project_id, topic_id)

    event_data = event.to_json().encode("utf-8")

    future = publisher.publish(topic_path, event_data)
    print(f"Published message ID: {future.result()}")
    return future.result()
