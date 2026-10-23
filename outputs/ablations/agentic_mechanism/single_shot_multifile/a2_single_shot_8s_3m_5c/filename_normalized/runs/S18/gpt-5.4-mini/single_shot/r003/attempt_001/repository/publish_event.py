import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import build_publisher, resolve_topic_path
from messaging_models import MessageEnvelope, normalize_json_payload


def publish_event(payload: Any, attributes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    topic_id = os.environ.get("PUBSUB_TOPIC")
    if not project_id or not topic_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT and PUBSUB_TOPIC are required")

    publisher = build_publisher()
    topic_path = resolve_topic_path(project_id, topic_id)
    envelope = MessageEnvelope(payload=normalize_json_payload(payload), attributes=attributes or {})
    data = json.dumps(envelope.payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    future = publisher.publish(topic_path, data=data, **envelope.attributes)
    message_id = future.result()
    return {"topic": topic_path, "message_id": message_id, "attributes": envelope.attributes}
