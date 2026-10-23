import os
from google.cloud import pubsub_v1
import json
from typing import Dict, Any


def publish_event(event_data: Dict[str, Any], topic_id: str = None) -> str:
    """Publish a JSON event to Google Cloud Pub/Sub topic."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    if topic_id is None:
        topic_id = os.environ.get("PUBSUB_TOPIC_ID", "customer-events")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    data = json.dumps(event_data).encode("utf-8")

    future = publisher.publish(topic_path, data)
    message_id = future.result()

    return message_id


if __name__ == "__main__":
    sample_event = {
        "event_type": "customer_signup",
        "customer_id": "cust_12345",
        "email": "customer@example.com",
        "timestamp": "2024-01-15T10:30:00Z",
    }

    try:
        message_id = publish_event(sample_event)
        print(f"Published event with message ID: {message_id}")
    except Exception as e:
        print(f"Failed to publish event: {e}")
