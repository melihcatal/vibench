from messaging_client import get_publisher, get_dead_letter_topic_path
from messaging_models import EventMessage, DeadLetterResponse, sanitize_attributes


def send_to_dead_letter(
    event_data: dict,
    failure_reason: str,
    retry_count: int = 0,
    dead_letter_topic_name: str = None,
) -> DeadLetterResponse:
    publisher = get_publisher()
    dead_letter_path = get_dead_letter_topic_path(dead_letter_topic_name)

    event = EventMessage.from_dict(event_data)
    dead_letter_payload = {
        **event.to_dict(),
        "failure_reason": failure_reason,
        "retry_count": retry_count,
        "original_event_id": event.event_id,
    }

    payload_bytes = str(dead_letter_payload).encode("utf-8")
    attributes = sanitize_attributes(
        {
            "event_type": event.event_type,
            "original_event_id": event.event_id,
            "failure_reason": failure_reason,
            "retry_count": str(retry_count),
            "dead_lettered": "true",
        }
    )

    try:
        future = publisher.publish(dead_letter_path, data=payload_bytes, **attributes)
        dead_letter_id = future.result()
        return DeadLetterResponse(
            success=True,
            dead_letter_id=dead_letter_id,
            original_event_id=event.event_id,
            destination_topic=dead_letter_path,
            failure_reason=failure_reason,
            retry_count=retry_count,
        )
    except Exception as exc:
        return DeadLetterResponse(
            success=False,
            original_event_id=event.event_id,
            destination_topic=dead_letter_path,
            failure_reason=str(exc),
            retry_count=retry_count,
        )


def dead_letter_from_consume_error(
    consume_response, error_reason: str, retry_count: int = 0
) -> DeadLetterResponse:
    if consume_response.event:
        event_data = consume_response.event.to_dict()
    else:
        event_data = {"event_id": "unknown", "payload": {}}
    return send_to_dead_letter(event_data, error_reason, retry_count)
