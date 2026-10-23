from messaging_models import EventMessage, DeadLetterResult
from messaging_client import (
    publish_message_to_topic,
    ensure_topic_exists,
    nack_message,
)


def send_to_dead_letter(
    dead_letter_topic_name: str,
    original_message: EventMessage,
    failure_reason: str,
    subscription_name: str = "",
    ack_id: str = "",
) -> DeadLetterResult:
    ensure_topic_exists(dead_letter_topic_name)
    dl_event = EventMessage(
        event_type=f"dead_letter.{original_message.event_type}",
        source="dead-letter-handler",
        payload={
            "original_event": original_message.to_dict(),
            "failure_reason": failure_reason,
        },
        attributes={
            "original_event_id": original_message.event_id,
            "original_event_type": original_message.event_type,
            "failure_reason": failure_reason,
        },
    )
    try:
        dl_message_id = publish_message_to_topic(
            dead_letter_topic_name, dl_event, dl_event.attributes
        )
        if subscription_name and ack_id:
            nack_message(subscription_name, ack_id)
        return DeadLetterResult(
            original_message_id=original_message.event_id,
            dead_letter_message_id=dl_message_id,
            success=True,
            dead_letter_topic=dead_letter_topic_name,
            failure_reason=failure_reason,
        )
    except Exception as e:
        return DeadLetterResult(
            original_message_id=original_message.event_id,
            success=False,
            error=str(e),
            dead_letter_topic=dead_letter_topic_name,
            failure_reason=failure_reason,
        )


if __name__ == "__main__":
    original = EventMessage(
        event_id="evt-001",
        event_type="order.placed",
        source="order-service",
        payload={"order_id": "ORD-999"},
    )
    result = send_to_dead_letter(
        dead_letter_topic_name="dead-letter-topic",
        original_message=original,
        failure_reason="Processing timeout exceeded",
    )
    print(result.to_dict())
