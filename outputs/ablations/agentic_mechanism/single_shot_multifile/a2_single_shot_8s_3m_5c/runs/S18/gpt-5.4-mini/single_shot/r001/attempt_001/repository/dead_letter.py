import json
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import get_project_id, get_topic_path, load_settings
from messaging_models import DeadLetterRequest, DeadLetterResponse, normalize_attributes, normalize_json_payload


def send_dead_letter(payload: Any, reason: str, attributes: Optional[Dict[str, Any]] = None, dead_letter_topic_id: Optional[str] = None) -> DeadLetterResponse:
    settings = load_settings()
    project_id = get_project_id(settings)
    topic_path = get_topic_path(project_id, dead_letter_topic_id or settings.dead_letter_topic_id)
    request = DeadLetterRequest(payload=payload, reason=reason, attributes=attributes or {})
    body = normalize_json_payload(request.payload)
    message_attributes = normalize_attributes(request.attributes)
    message_attributes["dead_letter_reason"] = request.reason
    publisher = pubsub_v1.PublisherClient()
    future = publisher.publish(topic_path, json.dumps(body, separators=(",", ":")).encode("utf-8"), **message_attributes)
    message_id = future.result()
    return DeadLetterResponse(topic=topic_path, message_id=message_id, reason=reason, payload=body, attributes=message_attributes)
