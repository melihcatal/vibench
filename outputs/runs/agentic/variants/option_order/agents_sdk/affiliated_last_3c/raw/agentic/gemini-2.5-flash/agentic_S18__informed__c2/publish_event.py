import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client

def publish_event(topic_id: str, event_data: dict, attributes: dict = None):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    publisher = get_publisher_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    topic_path = publisher.topic_path(project_id, topic_id)

    data_json = json.dumps(event_data).encode("utf-8")

    future = publisher.publish(topic_path, data_json, **(attributes or {}))
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS)
    # Ensure a topic named "my-event-topic" exists
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # python publish_event.py
    topic_id = "my-event-topic"
    event = {"message": "Hello, Pub/Sub!", "timestamp": "2023-10-27T10:00:00Z"}
    attrs = {"source": "example-app", "type": "greeting"}
    publish_event(topic_id, event, attrs)
