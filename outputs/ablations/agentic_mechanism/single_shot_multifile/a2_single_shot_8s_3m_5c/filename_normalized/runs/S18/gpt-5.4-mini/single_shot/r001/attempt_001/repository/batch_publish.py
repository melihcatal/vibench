import json
from typing import Any, Dict, Iterable, List, Optional

from google.cloud import pubsub_v1

from messaging_client import get_project_id, get_topic_path, load_settings
from messaging_models import BatchPublishRequest, BatchPublishResponse, normalize_attributes, normalize_json_payload


def batch_publish(messages: Iterable[Dict[str, Any]], topic_id: Optional[str] = None) -> BatchPublishResponse:
    settings = load_settings()
    project_id = get_project_id(settings)
    topic_path = get_topic_path(project_id, topic_id or settings.topic_id)
    request = BatchPublishRequest(messages=list(messages))
    publisher = pubsub_v1.PublisherClient()
    publish_ids: List[str] = []
    normalized_messages = []
    for item in request.messages:
        payload = normalize_json_payload(item.get("payload"))
        attributes = normalize_attributes(item.get("attributes") or {})
        normalized_messages.append({"payload": payload, "attributes": attributes})
        future = publisher.publish(topic_path, json.dumps(payload, separators=(",", ":")).encode("utf-8"), **attributes)
        publish_ids.append(future.result())
    return BatchPublishResponse(topic=topic_path, message_ids=publish_ids, messages=normalized_messages)
