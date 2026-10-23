"""
Send failed messages to a Google Cloud Pub/Sub dead-letter destination.

Uses the google-cloud-pubsub SDK to publish messages that have failed
processing to a dedicated dead-letter topic, authenticated via
GOOGLE_APPLICATION_CREDENTIALS.
"""

import json
from messaging_client import (
    get_publisher_client,
    topic_path,
    ensure_topic_exists,
    publish_message_sync,
)
from messaging_models import PubSubEvent, DeadLetterRecord


def send_to_dead_letter(
    original_message_id: str,
    event: PubSubEvent,
    failure_reason: str,
    retry_count: int = 0,
    dead_letter_topic_name: str | None = None,
) -> DeadLetterRecord:
    """
    Publish a failed message record to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        original_message_id: The Pub/Sub message ID of the original failed message.
        event: The PubSubEvent that failed processing.
        failure_reason: Description of why the message failed.
        retry_count: Number of prior delivery attempts.
        dead_letter_topic_name: Override the default dead-letter topic name.

    Returns:
        DeadLetterRecord with the published message ID and details.
    """
    record = DeadLetterRecord(
        original_message_id=original_message_id,
        event=event,
        failure_reason=failure_reason,
        retry_count=retry_count,
    )

    publisher = get_publisher_client()
    dl_topic = ensure_topic_exists(topic_name=dead_letter_topic_name)

    message_id = publish_message_sync(
        publisher=publisher,
        topic=dl_topic,
        data=record.to_bytes(),
        attributes={
            "original_message_id": original_message_id,
            "failure_reason": failure_reason,
            "retry_count": str(retry_count),
            "event_id": event.event_id,
            "event_type": event.event_type,
        },
    )

    record.original_message_id = original_message_id
    return record


def send_to_dead_letter_from_bytes(
    original_message_id: str,
    data: bytes,
    failure_reason: str,
    retry_count: int = 0,
    dead_letter_topic_name: str | None = None,
    attributes: dict[str, str] | None = None,
) -> DeadLetterRecord:
    """
    Send raw message bytes to a dead-letter topic. Useful when working
    directly with subscriber Message objects.

    Args:
        original_message_id: The Pub/Sub message ID.
        data: Raw message payload bytes.
        failure_reason: Why the message failed.
        retry_count: Number of delivery attempts.
        dead_letter_topic_name: Override default dead-letter topic.
        attributes: Additional Pub/Sub attributes for the dead-letter message.

    Returns:
        DeadLetterRecord with publication details.
    """
    event = PubSubEvent.from_bytes(data)

    record = DeadLetterRecord(
        original_message_id=original_message_id,
        event=event,
        failure_reason=failure_reason,
        retry_count=retry_count,
    )

    publisher = get_publisher_client()
    dl_topic = ensure_topic_exists(topic_name=dead_letter_topic_name)

    dl_attrs: dict[str, str] = {
        "original_message_id": original_message_id,
        "failure_reason": failure_reason,
        "retry_count": str(retry_count),
        "event_id": event.event_id,
        "event_type": event.event_type,
    }
    if attributes:
        dl_attrs.update(attributes)

    publish_message_sync(
        publisher=publisher,
        topic=dl_topic,
        data=record.to_bytes(),
        attributes=dl_attrs,
    )

    return record


if __name__ == "__main__":
    sample_event = PubSubEvent(
        event_type="order.payment_failed",
        payload={"order_id": "ord_789", "amount": 99.99, "currency": "USD"},
        source="payment_service",
    )
    result = send_to_dead_letter(
        original_message_id="msg_abc123",
        event=sample_event,
        failure_reason="Payment gateway timeout after 3 retries",
        retry_count=3,
    )
    print(json.dumps(result.to_dict(), indent=2, default=str))
