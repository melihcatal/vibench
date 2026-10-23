import os
import json
from google.cloud import pubsub_v1

def publish_json_event(project_id: str, topic_id: str, event_data: dict) -> None:
    """Publishes a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        project_id: The Google Cloud project ID.
        topic_id: The Pub/Sub topic ID.
        event_data: The JSON data to publish as a dictionary.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Data must be a bytestring
    data = json.dumps(event_data).encode("utf-8")

    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    topic_id = os.environ.get("PUBSUB_TOPIC_ID")

    if not project_id:
        print("Error: GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)
    if not topic_id:
        print("Error: PUBSUB_TOPIC_ID environment variable not set.")
        exit(1)

    # Example event data
    example_event = {
        "timestamp": "2026-09-20T10:00:00Z",
        "event_type": "user_login",
        "user_id": "12345",
        "ip_address": "192.168.1.1",
    }

    publish_json_event(project_id, topic_id, example_event)
