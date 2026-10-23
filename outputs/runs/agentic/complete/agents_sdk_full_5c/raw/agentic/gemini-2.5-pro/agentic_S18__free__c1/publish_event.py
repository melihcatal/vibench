import os
import json
from typing import Dict, Any

from messaging_client import get_publisher_client, get_topic_path
from messaging_models import EventMessage

def publish_event(event_payload: Dict[str, Any]):
    """
    Publishes a single event to a Google Cloud Pub/Sub topic.

    Args:
        event_payload: A dictionary representing the event payload.
    """
    topic_id = os.getenv("GCP_PUBSUB_TOPIC_ID")
    if not topic_id:
        raise ValueError("GCP_PUBSUB_TOPIC_ID environment variable not set.")

    publisher_client = get_publisher_client()
    topic_path = get_topic_path(publisher_client, topic_id)

    message = EventMessage(payload=event_payload)
    message_data = json.dumps(vars(message)).encode("utf-8")

    future = publisher_client.publish(topic_path, message_data, source="publish_event.py")
    
    print(f"Published message {future.result()} to {topic_path}.")
    return future.result()

if __name__ == '__main__':
    # This block is for demonstration and will not be executed in the test environment.
    # To run, set GCP_PROJECT_ID and GCP_PUBSUB_TOPIC_ID environment variables.
    # Example:
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # export GCP_PUBSUB_TOPIC_ID="your-topic-id"
    # python publish_event.py
    
    sample_payload = {"customer_id": "C12345", "order_total": 99.99}
    try:
        publish_event(sample_payload)
    except ValueError as e:
        print(e)
