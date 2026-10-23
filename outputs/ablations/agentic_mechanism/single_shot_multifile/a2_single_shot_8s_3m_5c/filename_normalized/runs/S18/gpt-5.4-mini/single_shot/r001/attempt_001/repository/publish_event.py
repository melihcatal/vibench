import json
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import get_project_id, get_topic_path, load_settings
from messaging_models import PublishEventRequest, PublishEventResponse, normalize_attributes, normalize_json_payload


def publish_event(payload: Any, attributes: Optional[Dict[str, Any]] = None, topic_id: Optional[str] = None) -> PublishEventResponse:
    settings = load_settings()
    project_id = get_project_id(settings)
    topic_path = get_topic_path(project_id, topic_id or settings.topic_id)
    request = PublishEventRequest(payload=payload, attributes=attributes or {})
    message_json = normalize_json_payload(request.payload)
    message_attributes = normalize_attributes(request.attributes)
    publisher = pubsub_v1.PublisherClient()
    data = json.dumps(message_json, separators=(",", ":")).encode("utf-8")
    future = publisher.publish(topic_path, data, **message_attributes)
    message_id = future.result()
    return PublishEventResponse(topic=topic_path, message_id=message_id, payload=message_json, attributes=message_attributes)
