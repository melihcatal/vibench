import json
import os
from google.cloud import pubsub_v1

from messaging_client import get_publisher_client

def publish_json_event(topic_id: str, data: dict, project_id: str = None):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(project_id or os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id)
    json_data = json.dumps(data).encode("utf-8")

    future = publisher.publish(topic_path, json_data, content_type="application/json")
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var set)
    # Ensure a topic named 'my-topic' exists in your project.
    # from your shell, run:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # python publish_event.py
    event_data = {"message": "Hello, Pub/Sub!", "timestamp": "2023-10-27T10:00:00Z"}
    publish_json_event("my-topic", event_data)
