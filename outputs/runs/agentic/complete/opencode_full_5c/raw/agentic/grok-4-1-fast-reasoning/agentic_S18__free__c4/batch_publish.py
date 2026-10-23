import json
from google.cloud import pubsub_v1
import messaging_client
from messaging_models import serialize_payload
from typing import Dict, Any, List, Optional


def batch_publish(
    events: List[Dict[str, Any]], message_ids: Optional[List[str]] = None
) -> List[str]:
    """
    Publishes a batch of messages with optional IDs as attributes.
    """
    try:
        client = pubsub_v1.PublisherClient()
        topic_path = client.topic_path(
            messaging_client.PUBSUB_PROJECT_ID, messaging_client.PUBSUB_TOPIC
        )
        result_ids = []
        ids_iter = message_ids or []
        for event, mid in zip(events, ids_iter):
            data = serialize_payload(event)
            attrs = {"custom_id": mid} if mid else {}
            future = client.publish(topic_path, data, **attrs)
            result_ids.append(future.result())
        return result_ids
    except Exception as e:
        return []
