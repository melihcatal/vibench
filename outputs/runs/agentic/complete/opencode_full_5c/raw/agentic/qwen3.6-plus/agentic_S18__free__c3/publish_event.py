import json
from messaging_client import get_publisher, get_topic_path
from messaging_models import EventMessage, PublishResponse, sanitize_attributes


def publish_event(event_data: dict, topic_name: str = None) -> PublishResponse:
    event = EventMessage.from_dict(event_data)
    publisher = get_publisher()
    topic_path = get_topic_path(topic_name)

    payload_bytes = event.to_json_bytes()
    attributes = sanitize_attributes(
        {
            "event_type": event.event_type,
            "event_id": event.event_id,
            "source": event.source,
            "correlation_id": event.correlation_id,
            **event.attributes,
        }
    )

    try:
        future = publisher.publish(topic_path, data=payload_bytes, **attributes)
        message_id = future.result()
        return PublishResponse(
            success=True,
            message_id=message_id,
            event_id=event.event_id,
            topic=topic_path,
        )
    except Exception as exc:
        return PublishResponse(
            success=False,
            event_id=event.event_id,
            topic=topic_path,
            error=str(exc),
        )


def publish_raw_event(
    payload: dict,
    event_type: str,
    source: str,
    topic_name: str = None,
    extra_attributes: dict = None,
) -> PublishResponse:
    event_data = {
        "event_type": event_type,
        "source": source,
        "payload": payload,
        "attributes": extra_attributes or {},
    }
    return publish_event(event_data, topic_name)
