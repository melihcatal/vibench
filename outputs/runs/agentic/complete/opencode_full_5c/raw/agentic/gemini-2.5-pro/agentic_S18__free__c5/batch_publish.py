import json
import os
from typing import List, Dict, Any
from google.cloud import pubsub_v1

from messaging_client import get_publisher_client, get_topic_path, get_project_id


def batch_publish(topic_id: str, messages: List[Dict[str, Any]]):
    """Publishes a batch of messages to a Google Cloud Pub/Sub topic."""
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    publisher = get_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    publish_futures = []
    for message_data in messages:
        data = json.dumps(message_data.get("data", {})).encode("utf-8")
        attributes = message_data.get("attributes", {})
        future = publisher.publish(topic_path, data, **attributes)
        publish_futures.append(future)

    results = [future.result() for future in publish_futures]
    return results


if __name__ == "__main__":
    # This is an example, and will not be executed.
    BATCH_TOPIC_ID = os.environ.get("PUB_SUB_TOPIC", "my-topic")

    message_list = [
        {"data": {"message": "Batch message 1"}, "attributes": {"id": "msg1"}},
        {"data": {"message": "Batch message 2"}, "attributes": {"id": "msg2"}},
        {"data": {"message": "Batch message 3"}, "attributes": {"id": "msg3"}},
    ]

    print(f"Publishing batch to {BATCH_TOPIC_ID}...")
    message_ids = batch_publish(BATCH_TOPIC_ID, message_list)
    print(f"Published messages with IDs: {message_ids}")
