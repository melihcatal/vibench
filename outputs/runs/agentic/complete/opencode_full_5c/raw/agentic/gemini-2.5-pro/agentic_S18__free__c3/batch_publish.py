import os
import json
from typing import List
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def batch_publish(topic_id: str, messages: List[Message]):
    """Publishes a batch of messages to a Google Cloud Pub/Sub topic."""
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    publish_futures = []

    for message in messages:
        data = json.dumps(message.data).encode("utf-8")
        future = publisher.publish(topic_path, data, **(message.attributes or {}))
        publish_futures.append(future)

    results = [future.result() for future in publish_futures]
    return results


if __name__ == "__main__":
    topic_id = os.environ.get("GCP_BATCH_TOPIC_ID", "default-batch-topic")

    messages_to_publish = [
        Message(
            data={"id": 1, "content": "First message"}, attributes={"batch": "true"}
        ),
        Message(
            data={"id": 2, "content": "Second message"}, attributes={"batch": "true"}
        ),
        Message(
            data={"id": 3, "content": "Third message"}, attributes={"batch": "true"}
        ),
    ]

    print(f"Publishing batch of {len(messages_to_publish)} messages to {topic_id}...")
    message_ids = batch_publish(topic_id, messages_to_publish)
    print(f"Published message IDs: {message_ids}")
