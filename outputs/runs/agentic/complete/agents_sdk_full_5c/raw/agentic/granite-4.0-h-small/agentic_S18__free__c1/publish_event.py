import os
import json
import google.cloud.pubsub_v1 as pubsub

from messaging_client import get_publisher_client
from messaging_models import EventMessage

def publish_event(topic_name: str, payload: dict):
    """Publish a single JSON event to a Pub/Sub topic.
    
    Uses Google Cloud Pub/Sub as the managed messaging provider.
    """
    publisher = get_publisher_client()
    # Ensure payload is a JSON-serializable dict
    message_data = json.dumps(payload).encode('utf-8')
    # Optional: add a unique attribute
    attributes = {"event_id": payload.get('event_id', 'unknown')}
    future = publisher.publish(topic_name, message_data, **attributes)
    print(f"Published event to {topic_name}: {attributes}")
    # Block on future to surface errors
    future.result()

if __name__ == "__main__":
    # Example usage
    topic = os.getenv("PUBSUB_TOPIC")
    if not topic:
        raise RuntimeError("Set PUBSUB_TOPIC environment variable")
    sample_payload = {
        "event_id": "evt_123",
        "user": "alice",
        "action": "login"
    }
    publish_event(topic, sample_payload)
