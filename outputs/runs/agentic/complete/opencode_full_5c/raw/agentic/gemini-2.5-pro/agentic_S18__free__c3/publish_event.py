import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path


def publish_event(topic_id: str, event_data: dict):
    """Publishes a single event to a Google Cloud Pub/Sub topic."""
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    data = json.dumps(event_data).encode("utf-8")

    future = publisher.publish(topic_path, data)
    return future.result()


if __name__ == "__main__":
    topic_id = os.environ.get("GCP_TOPIC_ID", "default-topic")
    sample_event = {"message": "Hello, World!", "user": "test-user"}
    print(f"Publishing event to {topic_id}...")
    message_id = publish_event(topic_id, sample_event)
    print(f"Published message with ID: {message_id}")
