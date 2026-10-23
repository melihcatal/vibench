import json
import os
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def publish_event(event: dict):
    publisher = get_publisher_client()
    topic_id = os.environ.get("GCP_TOPIC_ID", "my-topic")
    topic_path = get_topic_path(topic_id)

    message = Message(data=event)

    future = publisher.publish(
        topic_path, message.to_json(), **(message.attributes or {})
    )
    return future.result()


if __name__ == "__main__":
    # This is a placeholder for actual event data
    sample_event = {"user_id": "12345", "action": "login"}
    print(f"Publishing event: {sample_event}")
    message_id = publish_event(sample_event)
    print(f"Published message with ID: {message_id}")
