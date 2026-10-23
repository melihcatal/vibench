import json
from typing import Optional

from messaging_client import get_publisher_client, dead_letter_topic_path
from messaging_models import (
    DeadLetterResult,
    EventMessage,
    normalize_payload,
    build_event_attributes,
)


def send_to_dead_letter(
    original_message_id: str,
    failed_payload: dict,
    reason: str = "processing_failure",
    event_type: str = "dead_letter.event",
    source: str = "dead_letter_handler",
    dead_letter_topic_id: Optional[str] = None,
) -> DeadLetterResult:
    publisher = get_publisher_client()
    dlq_topic = dead_letter_topic_path(dead_letter_topic_id)

    payload = normalize_payload(failed_payload)
    event = EventMessage(
        event_type=event_type,
        source=source,
        payload={
            "original_payload": payload,
            "failure_reason": reason,
            "original_message_id": original_message_id,
        },
        attributes={
            "original_message_id": original_message_id,
            "failure_reason": reason,
        },
    )

    data_bytes = event.to_json().encode("utf-8")
    attributes = build_event_attributes(event)
    attributes["original_message_id"] = original_message_id
    attributes["failure_reason"] = reason

    future = publisher.publish(dlq_topic, data=data_bytes, **attributes)
    dead_letter_message_id = future.result(timeout=30.0)

    return DeadLetterResult(
        original_message_id=original_message_id,
        dead_letter_message_id=dead_letter_message_id,
        dead_letter_topic_path=dlq_topic,
        reason=reason,
    )


def send_to_dead_letter_from_event(
    event: EventMessage,
    reason: str = "processing_failure",
    dead_letter_topic_id: Optional[str] = None,
) -> DeadLetterResult:
    return send_to_dead_letter(
        original_message_id=event.event_id,
        failed_payload=event.payload,
        reason=reason,
        event_type=event.event_type,
        source=event.source,
        dead_letter_topic_id=dead_letter_topic_id,
    )


def send_to_dead_letter_from_json(
    original_message_id: str,
    json_string: str,
    reason: str = "processing_failure",
    dead_letter_topic_id: Optional[str] = None,
) -> DeadLetterResult:
    payload = json.loads(json_string)
    return send_to_dead_letter(
        original_message_id=original_message_id,
        failed_payload=payload,
        reason=reason,
        dead_letter_topic_id=dead_letter_topic_id,
    )
