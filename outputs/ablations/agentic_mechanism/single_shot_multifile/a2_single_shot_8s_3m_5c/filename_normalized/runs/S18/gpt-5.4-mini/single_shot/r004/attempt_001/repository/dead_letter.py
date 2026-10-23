import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import get_dead_letter_topic_path, get_publisher_client
from messaging_models import normalize_dead_letter_payload


def dead_letter(message: Dict[str, Any]) -> Dict[str, Any]:
    publisher = get_publisher_client()
    topic_path = get_dead_letter_topic_path()
    payload = normalize_dead_letter_payload(message)
    data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    future = publisher.publish(topic_path, data=data, failure_reason=str(payload.get("failure_reason", "unknown")))
    message_id = future.result()
    return {"message_id": message_id, "dead_letter_topic_path": topic_path, "payload": payload}
