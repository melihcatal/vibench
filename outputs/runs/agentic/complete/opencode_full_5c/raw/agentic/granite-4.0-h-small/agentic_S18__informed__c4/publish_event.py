import os
from messaging_client import get_pubsub_client, serialize_event


def publish_event(topic_name, event):
    """Publish a JSON event to the configured Pub/Sub topic.

    Uses the active provider's client (e.g., AWS SNS, GCP Pub/Sub, Azure Service Bus).
    """
    client = get_pubsub_client()
    payload = serialize_event(event)
    response = client.publish(topic_name, payload)
    print(f"Published event to {topic_name}: {response}")
