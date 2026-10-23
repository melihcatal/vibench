
from google.cloud import pubsub_v1
import json
import os

def publish_json_event(project_id: str, topic_id: str, event_data: dict):
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    json_payload = json.dumps(event_data).encode("utf-8")

    future = publisher.publish(topic_path, json_payload)
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and Topic ID
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    TOPIC_ID = "my-test-topic"  # Replace with your Pub/Sub topic ID

    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace PROJECT_ID with your actual project ID.")
    else:
        example_event = {
            "timestamp": "2026-09-20T10:00:00Z",
            "event_type": "user_login",
            "user_id": "12345",
            "details": {
                "ip_address": "192.168.1.1",
                "device": "mobile"
            }
        }
        publish_json_event(PROJECT_ID, TOPIC_ID, example_event)
