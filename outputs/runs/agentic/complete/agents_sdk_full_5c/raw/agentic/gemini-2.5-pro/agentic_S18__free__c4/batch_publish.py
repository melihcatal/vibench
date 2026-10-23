import json
import os
from typing import List
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import BaseMessage


def publish_batch(topic_id: str, messages: List[BaseMessage]):
    """
    Publishes a batch of messages to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The ID of the Pub/Sub topic.
        messages: A list of BaseMessage objects to publish.
    """
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)
    
    futures = []
    for msg in messages:
        data = msg.json().encode("utf-8")
        # Add message_id as an attribute for tracking
        attributes = {"message_id": msg.message_id}
        if msg.attributes:
            attributes.update(msg.attributes)
        
        future = publisher.publish(topic_path, data, **attributes)
        futures.append(future)

    published_ids = [future.result() for future in futures]
    print(f"Published {len(published_ids)} messages to {topic_path}.")
    return published_ids


if __name__ == "__main__":
    # This block is for demonstration and will not be executed in the test environment.
    TOPIC_ID = os.getenv("PUB_SUB_TOPIC_ID", "batch-topic")
    message_batch = [
        BaseMessage(content=json.dumps({"event": "start", "batch": "1"})),
        BaseMessage(content=json.dumps({"event": "process", "batch": "1"})),
        BaseMessage(content=json.dumps({"event": "end", "batch": "1"})),
    ]
    publish_batch(TOPIC_ID, message_batch)
