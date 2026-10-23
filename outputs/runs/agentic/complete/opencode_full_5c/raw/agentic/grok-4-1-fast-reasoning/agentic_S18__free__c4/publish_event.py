import json
from google.cloud import pubsub_v1
import messaging_client
from messaging_models import serialize_payload, pubsub_message_to_dict
from typing import Dict, Any, Optional


def publish_event(payload: Dict[str, Any]) -> Optional[str]:
    """
    Publishes a JSON event to the configured Pub/Sub topic.
    """
    try:
        client = pubsub_v1.PublisherClient()
        topic_path = client.topic_path(
            messaging_client.PUBSUB_PROJECT_ID, messaging_client.PUBSUB_TOPIC
        )
        data = serialize_payload(payload)
        future = client.publish(topic_path, data)
        return future.result()
    except Exception:
        return None
