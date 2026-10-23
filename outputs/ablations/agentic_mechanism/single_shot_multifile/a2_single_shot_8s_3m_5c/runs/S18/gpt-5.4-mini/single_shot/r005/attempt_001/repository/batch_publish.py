import json
from typing import Any, Dict, List

from google.cloud import pubsub_v1

from messaging_client import get_publisher_client, get_topic_path, load_settings
from messaging_models import BatchPublishRequest, normalize_event_payload


def batch_publish(request: Dict[str, Any]) -> Dict[str, Any]:
    settings = load_settings()
    parsed = BatchPublishRequest.from_mapping(request)
    client = get_publisher_client()
    topic_path = get_topic_path(client, settings.project_id, settings.topic_id)
    results: List[Dict[str, Any]] = []
    for item in parsed.messages:
        payload = normalize_event_payload(item.payload)
        data = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        future = client.publish(topic_path, data=data, **item.attributes)
        results.append({"correlation_id": item.correlation_id, "message_id": future.result(timeout=settings.timeout_seconds), "attributes": item.attributes})
    return {"provider": "google-cloud-pubsub", "topic": topic_path, "results": results}
