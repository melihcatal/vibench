import os
from typing import Dict, Any
from messaging_client import PubSubClient
from messaging_models import EventPayload

# Google Cloud Pub/Sub provider-identifying signal: google.cloud.pubsub_v1


def publish_event(
    topic_id: str,
    event_data: Dict[str, Any],
    event_type: str,
    source: str,
    event_id: Optional[str] = None,
) -> str:
    """Publishes a JSON event to a Google Cloud Pub/Sub topic."""
    client = PubSubClient()
    topic_path = client.get_topic_path(topic_id)

    payload = EventPayload(
        data=event_data, event_type=event_type, source=source, event_id=event_id
    )
    data = payload.to_json_string().encode("utf-8")

    future = client.publisher.publish(
        topic_path, data, event_type=event_type, source=source
    )
    message_id = future.result()  # Blocks until the message is published
    return message_id
