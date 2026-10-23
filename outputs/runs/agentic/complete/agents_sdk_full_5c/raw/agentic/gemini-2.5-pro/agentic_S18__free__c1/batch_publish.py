import os
import json
import time
import uuid
from typing import List, Dict, Any

from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path

def publish_message_batch(messages: List[Dict[str, Any]]):
    """
    Publishes a batch of messages to a Google Cloud Pub/Sub topic.

    Args:
        messages: A list of dictionaries, where each dictionary is a message payload.
    """
    topic_id = os.getenv("GCP_PUBSUB_TOPIC_ID")
    if not topic_id:
        raise ValueError("GCP_PUBSUB_TOPIC_ID environment variable not set.")

    publisher_client = get_publisher_client()
    topic_path = get_topic_path(publisher_client, topic_id)

    publish_futures = []

    for message_payload in messages:
        # Add a unique ID to each message attribute
        attributes = {"message_id": str(uuid.uuid4())}
        data = json.dumps(message_payload).encode("utf-8")
        
        # The client library automatically batches messages.
        # The publish method returns a future.
        future = publisher_client.publish(topic_path, data, **attributes)
        publish_futures.append(future)

    # Wait for all the publish futures to resolve.
    results = [future.result() for future in publish_futures]
    
    print(f"Published {len(results)} messages to {topic_path} with message IDs: {results}")
    return results

if __name__ == '__main__':
    # This block is for demonstration and will not be executed in the test environment.
    # To run, set GCP_PROJECT_ID and GCP_PUBSUB_TOPIC_ID environment variables.
    
    sample_messages = [
        {"item": "A", "quantity": 10},
        {"item": "B", "quantity": 5},
        {"item": "C", "quantity": 12},
    ]
    try:
        publish_message_batch(sample_messages)
    except ValueError as e:
        print(e)
