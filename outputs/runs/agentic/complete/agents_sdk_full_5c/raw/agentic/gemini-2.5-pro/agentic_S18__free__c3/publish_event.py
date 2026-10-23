import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path

def publish_event(event_data: dict):
    """Publishes a single JSON event to a Pub/Sub topic."""
    publisher, topic_path = get_publisher_client()
    
    # Data must be a bytestring
    data = json.dumps(event_data).encode("utf-8")
    
    future = publisher.publish(topic_path, data)
    print(f"Published message with ID: {future.result()}")
    return future.result()

if __name__ == '__main__':
    # Example Usage:
    sample_event = {
        "user_id": "user-123",
        "event_type": "login",
        "ip_address": "192.168.1.100"
    }
    if os.getenv("GCP_PROJECT_ID"):
        publish_event(sample_event)
    else:
        print("Set GCP_PROJECT_ID and other env vars to run.")
