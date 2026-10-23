import json
from google.cloud import pubsub_v1
import messaging_client
from messaging_models import serialize_payload
from typing import Dict, Any, Optional


def send_to_dead_letter(msg: Dict[str, Any]) -> Optional[str]:
    """
    Sends a failed message to the dead-letter Pub/Sub topic.
    """
    try:
        client = pubsub_v1.PublisherClient()
        dl_topic_path = client.topic_path(
            messaging_client.PUBSUB_PROJECT_ID, messaging_client.PUBSUB_DEADLETTER_TOPIC
        )
        data = serialize_payload(msg["payload"])
        attrs = msg.get("attributes", {}).copy()
        attrs["original_message_id"] = msg.get("message_id", "")
        attrs["dead_letter_time"] = json.dumps({"timestamp": "now"})
        future = client.publish(dl_topic_path, data, **attrs)
        return future.result()
    except Exception:
        return None
