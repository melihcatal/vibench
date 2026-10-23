import os
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client
from messaging_models import normalize_event

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
topic_name = os.getenv('PUBLISH_TOPIC', 'my-topic')

def publish_event(event: dict):
    """Publish a single JSON event to Google Cloud Pub/Sub.

    Args:
        event (dict): JSON-serializable event payload.
    """
    # Normalize payload
    payload = normalize_event(event)
    # Get client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    publisher = get_publisher_client()
    # Convert dict to bytes (JSON string)
    data = str(payload).encode('utf-8')
    # Publish
    future = publisher.publish(topic_name, data=data)
    # Optional: wait for ack
    try:
        message_id = future.result()
        print(f"Published message ID: {message_id}")
    except Exception as e:
        print(f"Error publishing event: {e}")
