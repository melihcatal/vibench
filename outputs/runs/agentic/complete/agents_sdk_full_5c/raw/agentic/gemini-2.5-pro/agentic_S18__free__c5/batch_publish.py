
import os
import json
from typing import List, Dict
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client

def publish_batch(messages: List[Dict]):
    """
    Publishes a batch of messages to a Google Cloud Pub/Sub topic.
    Each message is a dict that will be JSON encoded.

    Args:
        messages: A list of dictionaries, where each dict represents a message.
    """
    publisher = get_publisher_client()
    project_id = os.environ["GCP_PROJECT_ID"]
    topic_id = os.environ["GCP_TOPIC_ID"]
    topic_path = publisher.topic_path(project_id, topic_id)

    publish_futures = []

    for i, message_data in enumerate(messages):
        # Ensure message_data has an ID for tracking
        if 'message_id' not in message_data:
            raise ValueError("Each message in the batch must have a 'message_id' key.")
        
        data_str = json.dumps(message_data)
        data = data_str.encode("utf-8")
        
        # Add attributes, like a batch sequence number
        attributes = {
            "batch_id": "batch-001",
            "sequence_number": str(i + 1)
        }
        
        future = publisher.publish(topic_path, data, **attributes)
        publish_futures.append(future)

    # Wait for all the publish futures to resolve.
    results = []
    for i, future in enumerate(publish_futures):
        try:
            message_id = future.result()
            print(f"Published message {messages[i]['message_id']} with server-generated ID: {message_id}")
            results.append(message_id)
        except Exception as e:
            print(f"Failed to publish message {messages[i]['message_id']}: {e}")
            results.append(None)
    
    return results

if __name__ == '__main__':
    # Example Usage:
    # Set the following environment variables before running:
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # export GCP_TOPIC_ID="your-topic-id"

    # batch_of_messages = [
    #     {"message_id": "msg-a-001", "content": "First message in batch."},
    #     {"message_id": "msg-a-002", "content": "Second message in batch."},
    #     {"message_id": "msg-a-003", "content": "Third message in batch."},
    # ]
    # publish_batch(batch_of_messages)
    pass
