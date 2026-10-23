import os
from messaging_client import PubSubClient


def publish_event(topic_name, event_json):
    """Publish a JSON event to a managed Pub/Sub topic using the configured provider.

    Args:
        topic_name (str): The fully qualified topic identifier (e.g., projects/my-project/topics/my-topic).
        event_json (dict): The event payload as a dictionary.
    """
    client = PubSubClient()
    # Normalize payload (optional)
    normalized = client.normalize_payload(event_json)
    response = client.publish(topic_name, normalized)
    print(f"Published event to {topic_name}: {response}")
