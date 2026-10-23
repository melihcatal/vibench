import json
import os
from typing import List
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def batch_publish(topic_id: str, messages: List[Message]):
    """
    Publishes a batch of messages to a Google Cloud Pub/Sub topic.
    """
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    futures = []

    for message in messages:
        data = json.dumps(message.data).encode("utf-8")
        future = publisher.publish(topic_path, data, **(message.attributes or {}))
        futures.append(future)

    message_ids = [future.result() for future in futures]
    print(f"Published {len(message_ids)} messages in a batch to {topic_path}.")
    return message_ids


if __name__ == "__main__":
    TOPIC_ID = os.environ.get("GCP_TOPIC_ID", "default-topic")

    messages_to_publish = [
        Message(data={"item_id": "abc", "quantity": 10}, attributes={"source": "api"}),
        Message(
            data={"item_id": "def", "quantity": 5}, attributes={"source": "inventory"}
        ),
        Message(data={"item_id": "ghi", "quantity": 7}, attributes={"source": "api"}),
    ]

    batch_publish(TOPIC_ID, messages_to_publish)
