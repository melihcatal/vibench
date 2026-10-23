from messaging_client import get_publisher, get_topic_path
from messaging_models import EventMessage, BatchPublishResponse, sanitize_attributes


def batch_publish(events_data: list, topic_name: str = None) -> BatchPublishResponse:
    publisher = get_publisher()
    topic_path = get_topic_path(topic_name)

    message_ids = []
    event_ids = []
    errors = []

    for idx, event_data in enumerate(events_data):
        event = EventMessage.from_dict(event_data)
        payload_bytes = event.to_json_bytes()
        attributes = sanitize_attributes(
            {
                "event_type": event.event_type,
                "event_id": event.event_id,
                "source": event.source,
                "batch_index": str(idx),
                **event.attributes,
            }
        )

        try:
            future = publisher.publish(topic_path, data=payload_bytes, **attributes)
            msg_id = future.result()
            message_ids.append(msg_id)
            event_ids.append(event.event_id)
        except Exception as exc:
            errors.append(
                {
                    "event_id": event.event_id,
                    "index": idx,
                    "error": str(exc),
                }
            )

    return BatchPublishResponse(
        success=len(errors) == 0,
        message_ids=message_ids,
        event_ids=event_ids,
        total_published=len(message_ids),
        total_failed=len(errors),
        topic=topic_path,
        errors=errors,
    )


def batch_publish_typed(
    events_with_types: list, source: str, topic_name: str = None
) -> BatchPublishResponse:
    events_data = []
    for item in events_with_types:
        events_data.append(
            {
                "event_type": item.get("event_type", "generic"),
                "source": source,
                "payload": item.get("payload", {}),
                "attributes": item.get("attributes", {}),
            }
        )
    return batch_publish(events_data, topic_name)
