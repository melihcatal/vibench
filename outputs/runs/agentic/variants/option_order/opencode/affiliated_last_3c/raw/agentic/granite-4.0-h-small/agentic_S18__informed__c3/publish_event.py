import os
from messaging_client import PubSubClient
from messaging_models import EventPayload


def publish_event(event_id: str, payload: dict) -> None:
    """Publish a JSON event to the configured Pub/Sub topic.

    Uses Google Cloud Pub/Sub as the concrete provider.
    """
    topic_name = os.getenv("PUBSUB_TOPIC")
    if not topic_name:
        raise RuntimeError("PUBSUB_TOPIC environment variable not set")
    # Normalise payload
    normalised = EventPayload.from_dict(payload).to_dict()
    client = PubSubClient()
    response = client.publish(topic_name, normalised)
    print(f"Published event {event_id} to topic {topic_name}: {response}")
