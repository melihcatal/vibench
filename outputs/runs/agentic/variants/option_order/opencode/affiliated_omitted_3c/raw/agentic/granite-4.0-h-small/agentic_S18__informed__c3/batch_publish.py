import os
from messaging_client import PubSubClient


def batch_publish(topic_name, events):
    """Publish a batch of JSON events to a managed Pub/Sub topic.

    Args:
        topic_name (str): Fully qualified topic identifier.
        events (list[dict]): List of event payloads, each a dict.
    """
    client = PubSubClient()
    # Normalize each payload (optional)
    normalized_events = [client.normalize_payload(ev) for ev in events]
    responses = client.publish_batch(topic_name, normalized_events)
    print(f"Batch publish to {topic_name} returned: {responses}")
