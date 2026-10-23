import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import get_publisher_client, get_topic_path, load_settings
from messaging_models import DeadLetterRequest, normalize_event_payload


def dead_letter(request: Dict[str, Any]) -> Dict[str, Any]:
    settings = load_settings()
    parsed = DeadLetterRequest.from_mapping(request)
    payload = normalize_event_payload(parsed.payload)
    payload["dead_letter_reason"] = parsed.reason
    client = get_publisher_client()
    topic_path = get_topic_path(client, settings.project_id, settings.dead_letter_topic_id)
    data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    message_id = client.publish(topic_path, data=data, reason=parsed.reason, source_message_id=parsed.source_message_id).result(timeout=settings.timeout_seconds)
    return {"provider": "google-cloud-pubsub", "dead_letter_topic": topic_path, "message_id": message_id}
