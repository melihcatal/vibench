import os
import json
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def publish_event(topic_id: str, event: Message):
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    data = json.dumps(event.data).encode("utf-8")

    future = publisher.publish(topic_path, data, **(event.attributes or {}))
    message_id = future.result()
    print(f"Published message {message_id} to {topic_path}")
    return message_id


if __name__ == "__main__":
    topic_id = os.environ.get("PUBSUB_TOPIC_ID")
    if not topic_id:
        raise ValueError("PUBSUB_TOPIC_ID environment variable not set.")

    sample_event = Message(
        data={"user_id": "user-123", "action": "login"},
        attributes={"source": "webapp", "version": "1.0"},
    )

    publish_event(topic_id, sample_event)
