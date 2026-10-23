import json
from messaging_client import (
    load_config,
    get_publisher_client,
    build_dead_letter_topic_path,
    publish_raw_message,
)
from messaging_models import EventMessage, DeadLetterResult, sanitize_event_attributes


def send_to_dead_letter(
    original_event: EventMessage,
    failure_reason: str,
    error_details: str = "",
) -> DeadLetterResult:
    config = load_config()
    publisher = get_publisher_client()
    dlq_topic_path = build_dead_letter_topic_path(config)

    dead_letter_payload = {
        "original_event_id": original_event.event_id,
        "original_event_type": original_event.event_type,
        "original_source": original_event.source,
        "original_timestamp": original_event.timestamp,
        "original_payload": original_event.payload,
        "failure_reason": failure_reason,
        "error_details": error_details,
        "dead_lettered_at": original_event.timestamp,
    }

    dl_event = EventMessage(
        event_type="dead_letter",
        source="dead-letter-handler",
        payload=dead_letter_payload,
        attributes={
            "original_event_id": original_event.event_id,
            "failure_reason": failure_reason,
        },
    )

    payload_bytes = dl_event.to_json().encode("utf-8")
    attributes = sanitize_event_attributes(
        {
            "original_event_id": original_event.event_id,
            "failure_reason": failure_reason,
            "event_type": "dead_letter",
        }
    )

    dead_letter_message_id = publish_raw_message(
        publisher, dlq_topic_path, payload_bytes, attributes
    )

    return DeadLetterResult(
        original_message_id=original_event.event_id,
        dead_letter_message_id=dead_letter_message_id,
        reason=failure_reason,
        status="dead_lettered",
    )


if __name__ == "__main__":
    sample_event = EventMessage(
        event_id="evt-abc-123",
        event_type="payment.processed",
        source="payment-service",
        payload={"transaction_id": "TXN-999", "amount": 50.00},
    )
    result = send_to_dead_letter(
        sample_event,
        failure_reason="schema_validation_failed",
        error_details="Missing required field: currency",
    )
    print(json.dumps(result.to_dict(), indent=2))
