import json
from typing import Optional

from messaging_client import get_publisher_client, topic_path
from messaging_models import (
    EventMessage,
    PublishResult,
    normalize_payload,
    build_event_attributes,
)


def publish_event(
    event_data: dict,
    event_type: str = "custom.event",
    source: str = "application",
    correlation_id: str = "",
    topic_id: Optional[str] = None,
) -> PublishResult:
    publisher = get_publisher_client()
    topic = topic_path(topic_id)

    payload = normalize_payload(event_data)
    event = EventMessage(
        event_type=event_type,
        source=source,
        payload=payload,
        correlation_id=correlation_id,
    )

    data_bytes = event.to_json().encode("utf-8")
    attributes = build_event_attributes(event)

    future = publisher.publish(topic, data=data_bytes, **attributes)
    message_id = future.result(timeout=30.0)

    return PublishResult(
        message_id=message_id,
        event_id=event.event_id,
        status="published",
        topic_path=topic,
    )


def publish_event_from_json(
    json_string: str,
    event_type: str = "custom.event",
    source: str = "application",
    topic_id: Optional[str] = None,
) -> PublishResult:
    event_data = json.loads(json_string)
    return publish_event(
        event_data=event_data,
        event_type=event_type,
        source=source,
        topic_id=topic_id,
    )
