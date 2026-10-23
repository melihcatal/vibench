import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import publisher_client, topic_path
from messaging_models import PublishRequest, PublishResponse, normalize_payload


def publish_event(topic: str, event: Dict[str, Any], attributes: Dict[str, str] | None = None) -> PublishResponse:
    client = publisher_client()
    request = PublishRequest(topic=topic_path(topic), event=normalize_payload(event), attributes=attributes or {})
    future = client.publish(request.topic, json.dumps(request.event).encode("utf-8"), **request.attributes)
    message_id = future.result()
    return PublishResponse(message_id=message_id, topic=request.topic)


def handler(topic: str, event: Dict[str, Any]) -> Dict[str, Any]:
    response = publish_event(topic, event)
    return {"message_id": response.message_id, "topic": response.topic}
