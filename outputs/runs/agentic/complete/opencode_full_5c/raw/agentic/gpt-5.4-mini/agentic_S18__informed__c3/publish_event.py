import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import encode_message, get_project_id, topic_path, to_attributes
from messaging_models import PublishRequest, PublishResponse, normalize_payload


def publish_event(
    topic: str, payload: Dict[str, Any], attributes: Optional[Dict[str, str]] = None
) -> PublishResponse:
    project_id = get_project_id()
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is required")
    publisher = pubsub_v1.PublisherClient()
    request = PublishRequest(
        topic=topic, payload=normalize_payload(payload), attributes=attributes
    )
    future = publisher.publish(
        topic_path(project_id, request.topic),
        encode_message(request.payload),
        **to_attributes(request.attributes),
    )
    return PublishResponse(message_id=future.result())
