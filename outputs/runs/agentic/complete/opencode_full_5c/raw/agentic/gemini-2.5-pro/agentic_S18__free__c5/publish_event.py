import json
import os
from messaging_client import get_publisher_client, get_topic_path, get_project_id
from messaging_models import PubSubMessage


def publish_event(topic_id: str, event_data: dict):
    """Publishes a single event to a Google Cloud Pub/Sub topic."""
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    publisher = get_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    message = PubSubMessage(data=event_data)

    data = json.dumps(message.data).encode("utf-8")

    future = publisher.publish(topic_path, data)
    return future.result()


if __name__ == "__main__":
    # This is an example, and will not be executed.
    TOPIC_ID = os.environ.get("PUB_SUB_TOPIC", "my-topic")
    sample_event = {"message": "Hello World", "user_id": 12345}
    print(f"Publishing event to {TOPIC_ID}...")
    message_id = publish_event(TOPIC_ID, sample_event)
    print(f"Published message with ID: {message_id}")
