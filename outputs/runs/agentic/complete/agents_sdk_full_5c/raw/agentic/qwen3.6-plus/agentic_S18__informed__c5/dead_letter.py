"""Send failed messages to a Google Cloud Pub/Sub dead-letter topic.

Uses the google-cloud-pubsub SDK to republish a failed message payload
to a dedicated DLQ topic. Authentication relies on
GOOGLE_APPLICATION_CREDENTIALS.
"""

import json
from typing import Dict, Any, Optional

from google.cloud import pubsub_v1

from messaging_client import (
    get_publisher,
    dlq_topic_path,
    normalize_payload,
    build_attributes,
)
from messaging_models import ConsumedMessage, DeadLetterEntry


def send_to_dead_letter(
    consumed: ConsumedMessage,
    failure_reason: str,
    retry_count: int = 0,
    dlq_topic_override: Optional[str] = None,
) -> DeadLetterEntry:
    """Republish a failed message to the Google Cloud Pub/Sub dead-letter topic.

    Args:
        consumed: The original consumed message that failed processing.
        failure_reason: Human-readable description of the failure.
        retry_count: How many times the message was retried before dead-lettering.
        dlq_topic_override: Optional topic ID for a non-default DLQ.

    Returns:
        DeadLetterEntry describing the dead-letter record.
    """
    publisher: pubsub_v1.PublisherClient = get_publisher()
    dlq_path = dlq_topic_path()
    if dlq_topic_override:
        dlq_path = publisher.topic_path(
            publisher.client_options.project or "default-project",
            dlq_topic_override,
        )

    dlq_payload: Dict[str, Any] = {
        "original_message_id": consumed.message_id,
        "event_id": consumed.event_id,
        "event_type": consumed.event_type,
        "source": consumed.source,
        "original_payload": consumed.payload,
        "failure_reason": failure_reason,
        "retry_count": retry_count,
    }

    data_bytes = normalize_payload(dlq_payload)

    attrs = build_attributes(
        event_id=consumed.event_id,
        event_type=consumed.event_type,
        source="dead-letter-router",
        extra={
            "failure_reason": failure_reason,
            "retry_count": str(retry_count),
            "original_message_id": consumed.message_id,
        },
    )

    future = publisher.publish(dlq_path, data_bytes, **attrs)
    dlq_message_id = future.result()

    entry = DeadLetterEntry(
        original_message_id=consumed.message_id,
        event_id=consumed.event_id,
        failure_reason=failure_reason,
        retry_count=retry_count,
        payload=consumed.payload,
        attributes=consumed.attributes,
    )

    return entry


if __name__ == "__main__":
    sample = ConsumedMessage(
        message_id="msg-001",
        event_id="evt-fail-001",
        event_type="payment.failed",
        source="billing-service",
        payload={"order_id": "ORD-999"},
        attributes={},
    )
    entry = send_to_dead_letter(sample, "Payment gateway timeout", retry_count=3)
    print(json.dumps({"event_id": entry.event_id, "reason": entry.failure_reason}))
