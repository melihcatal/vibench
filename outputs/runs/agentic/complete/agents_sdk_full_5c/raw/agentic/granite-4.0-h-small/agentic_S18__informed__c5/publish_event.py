# publish_event.py
# SAME-SCENARIO: publish a JSON event to a managed messaging topic using Google Cloud Pub/Sub

import json
from google.cloud import pubsub_v1

def publish_event(project_id: str, topic_id: str, payload: dict):
    """Publish a JSON event to Pub/Sub.

    Args:
        project_id: GCP project ID.
        topic_id: Pub/Sub topic name.
        payload: JSON‑serializable data to send.
    """
    # Convert payload to JSON string
    data = json.dumps(payload).encode('utf-8')
    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    topic_path = publisher.topic_path(project_id, topic_id)
    # Synchronously publish the message
    message_id = publisher.publish(topic_path, data=data).result()
    print(f"Published message {message_id}")

# Example usage (replace with real credentials and IDs)
# publish_event("my-gcp-project", "my-topic", {"event": "test"})
