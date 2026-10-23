import json
import os
from messaging_client import get_publisher_client, get_topic_path


def publish_event(topic_id: str, event_data: dict):
    """
    Publishes a single JSON event to a Google Cloud Pub/Sub topic.
    """
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    data = json.dumps(event_data).encode("utf-8")

    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")
    return future.result()


if __name__ == "__main__":
    TOPIC_ID = os.environ.get("GCP_TOPIC_ID", "default-topic")
    example_event = {"user_id": "user123", "action": "login", "status": "success"}
    publish_event(TOPIC_ID, example_event)
