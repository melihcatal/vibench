import json
import os
from typing import Dict, Any

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError

from messaging_client import get_publisher_client, get_topic_path

def publish_message(publisher: pubsub_v1.PublisherClient, topic_path: str, data: Dict[str, Any], attributes: Dict[str, str] = None):
    """Publishes a single message to a Pub/Sub topic."""
    try:
        payload = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, data=payload, **(attributes or {}))
        message_id = future.result()
        print(f"Published message {message_id} to {topic_path}")
        return message_id
    except GoogleAPICallError as e:
        print(f"Error publishing message to {topic_path}: {e}")
        raise

if __name__ == '__main__':
    # This is an example and will not be executed in the test environment
    # Required environment variables: GOOGLE_PROJECT_ID, MY_TOPIC_ID
    topic_id = os.environ.get("MY_TOPIC_ID")
    if topic_id:
        client = get_publisher_client()
        path = get_topic_path(topic_id)
        event_data = {"customer_id": "12345", "event_type": "order_placed"}
        event_attributes = {"source": "e-commerce-backend"}
        publish_message(client, path, event_data, event_attributes)
    else:
        print("MY_TOPIC_ID environment variable not set. Skipping example.")
