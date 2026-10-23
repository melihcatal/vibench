import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import build_publisher, resolve_topic_path
from messaging_models import MessageEnvelope, normalize_json_payload


def dead_letter(payload: Any, attributes: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    topic_id = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC")
    if not project_id or not topic_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT and PUBSUB_DEAD_LETTER_TOPIC are required")

    publisher = build_publisher()
    topic_path = resolve_topic_path(project_id, topic_id)
    dead_letter_attrs = dict(attributes or {})
    dead_letter_attrs["dead_letter"] = "true"
    envelope = MessageEnvelope(payload=normalize_json_payload(payload), attributes=dead_letter_attrs)
    data = json.dumps(envelope.payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    message_id = publisher.publish(topic_path, data=data, **envelope.attributes).result()
    return {"topic": topic_path, "message_id": message_id, "attributes": envelope.attributes}
