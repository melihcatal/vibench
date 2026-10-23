
from google.cloud import pubsub_v1
import json
import os

def publish_json_event(project_id: str, topic_id: str, message: dict):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    message_json = json.dumps(message)
    message_bytes = message_json.encode("utf-8")

    future = publisher.publish(topic_path, message_bytes)
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud Project ID and Topic ID here
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    topic_id = "my-topic"  # Replace with your Pub/Sub topic ID

    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'os.environ.get("GOOGLE_CLOUD_PROJECT")' with your project ID.")
    else:
        sample_message = {"event_type": "user_registered", "user_id": "12345", "timestamp": "2026-09-20T12:00:00Z"}
        publish_json_event(project_id, topic_id, sample_message)
