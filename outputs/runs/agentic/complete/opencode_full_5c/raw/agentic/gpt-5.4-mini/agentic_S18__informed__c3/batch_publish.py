from typing import Any, Dict, Iterable, List, Optional

from google.cloud import pubsub_v1

from messaging_client import encode_message, get_project_id, topic_path, to_attributes
from messaging_models import BatchPublishRequest, PublishResponse, normalize_payload


def batch_publish(topic: str, messages: List[Dict[str, Any]]) -> List[PublishResponse]:
    project_id = get_project_id()
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is required")
    publisher = pubsub_v1.PublisherClient()
    request = BatchPublishRequest(topic=topic, messages=messages)
    topic_full_path = topic_path(project_id, request.topic)
    futures = []
    for item in request.messages:
        payload = normalize_payload(item.get("payload"))
        attributes = to_attributes(item.get("attributes"))
        futures.append(
            publisher.publish(topic_full_path, encode_message(payload), **attributes)
        )
    return [PublishResponse(message_id=f.result()) for f in futures]
