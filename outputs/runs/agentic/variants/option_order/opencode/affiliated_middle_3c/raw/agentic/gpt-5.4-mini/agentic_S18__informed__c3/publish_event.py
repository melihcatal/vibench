import json

from messaging_client import get_publisher, topic_path
from messaging_models import (
    MessageRequest,
    MessageResponse,
    normalize_attributes,
    normalize_payload,
)


def publish_event(request: MessageRequest) -> MessageResponse:
    publisher = get_publisher()
    future = publisher.publish(
        topic_path(request.topic),
        data=normalize_payload(request.payload).encode("utf-8"),
        **normalize_attributes(request.attributes),
    )
    message_id = future.result()
    return MessageResponse(
        message_id=message_id,
        status="published",
        attributes=normalize_attributes(request.attributes),
    )


def publish_json_event(
    topic: str, payload: dict, attributes: dict | None = None
) -> MessageResponse:
    return publish_event(
        MessageRequest(
            topic=topic, payload=json.dumps(payload), attributes=attributes or {}
        )
    )
