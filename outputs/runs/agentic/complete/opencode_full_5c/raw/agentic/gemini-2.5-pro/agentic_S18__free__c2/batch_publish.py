import os
import json
from typing import List
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def publish_batch(topic_id: str, messages: List[Message]):
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    publish_futures = []
    for message in messages:
        data = json.dumps(message.data).encode("utf-8")
        future = publisher.publish(topic_path, data, **(message.attributes or {}))
        publish_futures.append(future)

    results = [future.result() for future in publish_futures]

    print(f"Published {len(results)} messages to {topic_path}.")
    for message_id in results:
        print(f"  - {message_id}")

    return results


if __name__ == "__main__":
    topic_id = os.environ.get("PUBSUB_TOPIC_ID")
    if not topic_id:
        raise ValueError("PUBSUB_TOPIC_ID environment variable not set.")

    batch_messages = [
        Message(data={"id": 1, "content": "first message"}, attributes={"batch": "A"}),
        Message(data={"id": 2, "content": "second message"}, attributes={"batch": "A"}),
        Message(data={"id": 3, "content": "third message"}, attributes={"batch": "A"}),
    ]

    publish_batch(topic_id, batch_messages)
