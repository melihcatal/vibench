import os
from messaging_client import PubSubClient
from typing import List, Dict
from messaging_models import EventPayload


def batch_publish(event_ids: List[str], payloads: List[Dict]) -> None:
    """Publish a batch of events to the Pub/Sub topic.

    Uses Google Cloud Pub/Sub as the concrete provider.
    """
    if len(event_ids) != len(payloads):
        raise ValueError("event_ids and payloads must have the same length")
    topic_name = os.getenv("PUBSUB_TOPIC")
    if not topic_name:
        raise RuntimeError("PUBSUB_TOPIC environment variable not set")
    client = PubSubClient()
    # Normalise each payload
    normalized = [EventPayload.from_dict(p).to_dict() for p in payloads]
    responses = client.publish_batch(topic_name, normalized)
    print(f"Batch published {len(responses)} messages to {topic_name}")
