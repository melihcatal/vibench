import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import get_publish_topic_path, get_publisher_client
from messaging_models import normalize_event_payload


def publish_event(event: Dict[str, Any]) -> Dict[str, Any]:
    publisher = get_publisher_client()
    topic_path = get_publish_topic_path()
    payload = normalize_event_payload(event)
    data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    future = publisher.publish(topic_path, data=data, event_type=str(payload.get("event_type", "message")))
    message_id = future.result()
    return {"message_id": message_id, "topic_path": topic_path, "payload": payload}
