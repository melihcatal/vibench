import json
from typing import Any, Dict, List

from messaging_client import publisher_client, topic_path
from messaging_models import BatchPublishRequest, PublishResponse, normalize_payload


def batch_publish(topic: str, messages: List[Dict[str, Any]]) -> List[PublishResponse]:
    client = publisher_client()
    request = BatchPublishRequest(topic=topic_path(topic), messages=messages)
    responses: List[PublishResponse] = []
    for item in request.messages:
        normalized = normalize_payload(item.get("payload", item))
        attrs = {k: str(v) for k, v in item.get("attributes", {}).items()}
        message_id = client.publish(request.topic, json.dumps(normalized).encode("utf-8"), **attrs).result()
        responses.append(PublishResponse(message_id=message_id, topic=request.topic))
    return responses
