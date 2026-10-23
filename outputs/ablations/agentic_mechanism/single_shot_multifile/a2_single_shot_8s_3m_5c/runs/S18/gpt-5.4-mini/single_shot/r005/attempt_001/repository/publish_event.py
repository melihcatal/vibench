import json
import os
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import get_publisher_client, get_topic_path, load_settings
from messaging_models import PublishEventRequest, normalize_event_payload


def publish_event(request: Dict[str, Any]) -> Dict[str, Any]:
    settings = load_settings()
    parsed = PublishEventRequest.from_mapping(request)
    payload = normalize_event_payload(parsed.payload)
    client = get_publisher_client()
    topic_path = get_topic_path(client, settings.project_id, settings.topic_id)
    data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    future = client.publish(topic_path, data=data, **parsed.attributes)
    message_id = future.result(timeout=settings.timeout_seconds)
    return {"provider": "google-cloud-pubsub", "topic": topic_path, "message_id": message_id, "attributes": parsed.attributes}
