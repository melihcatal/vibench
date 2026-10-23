"""Sends failed messages to a Google Cloud Pub/Sub dead-letter destination.

Uses the google.cloud.pubsub_v1 PublisherClient to republish messages that have
exceeded the retry threshold to a dedicated dead-letter topic for later inspection.
"""

import json
from datetime import datetime, timezone

from google.cloud.pubsub_v1 import PublisherClient

from messaging_client import (
    get_publisher_client,
    dead_letter_topic_path,
    get_max_retries,
)
from messaging_models import (
    PubSubEvent,
    ConsumeResult,
    DeadLetterRecord,
    build_message_attributes,
)


def send_to_dead_letter(
    consume_result: ConsumeResult,
    failure_reason: str,
    project_id: str | None = None,
    dead_letter_topic_id: str | None = None,
    client: PublisherClient | None = None,
) -> DeadLetterRecord:
    """Send a failed message to the Google Cloud Pub/Sub dead-letter topic.

    Takes a consumed message that has failed processing and republishes it
    to a dead-letter topic with failure metadata as attributes.

    Args:
        consume_result: The ConsumeResult from a failed message consumption.
        failure_reason: Description of why the message processing failed.
        project_id: GCP project ID. Uses default if not provided.
        dead_letter_topic_id: Dead-letter topic ID. Uses default if not provided.
        client: Optional pre-configured PublisherClient.

    Returns:
        DeadLetterRecord with details of the dead-lettered message.

    Raises:
        Exception: If publishing to the dead-letter topic fails.
    """
    publisher = client or get_publisher_client()
    dl_topic = dead_letter_topic_path(project_id, dead_letter_topic_id)

    event = consume_result.event
    max_retries = get_max_retries()

    dead_letter_payload = {
        "original_event": {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "source": event.source,
            "payload": event.payload,
            "created_at": event.created_at,
        },
        "failure_reason": failure_reason,
        "retry_count": consume_result.delivery_attempt,
        "max_retries": max_retries,
        "dead_lettered_at": datetime.now(timezone.utc).isoformat(),
    }

    data = json.dumps(dead_letter_payload).encode("utf-8")

    attributes = build_message_attributes(
        event_type=f"dead_letter.{event.event_type}",
        source="dead-letter-handler",
        extra={
            "original_event_id": event.event_id,
            "original_source": event.source,
            "failure_reason": failure_reason,
            "retry_count": str(consume_result.delivery_attempt),
            "max_retries": str(max_retries),
        },
    )

    future = publisher.publish(dl_topic, data, **attributes)
    dl_message_id = future.result()

    record = DeadLetterRecord(
        original_event_id=event.event_id,
        failure_reason=failure_reason,
        retry_count=consume_result.delivery_attempt,
        dead_letter_message_id=dl_message_id,
        original_topic=consume_result.event.source,
    )

    return record


def send_raw_to_dead_letter(
    event_id: str,
    event_type: str,
    payload: dict,
    source: str,
    failure_reason: str,
    retry_count: int,
    project_id: str | None = None,
    dead_letter_topic_id: str | None = None,
    client: PublisherClient | None = None,
) -> DeadLetterRecord:
    """Send a failed event to dead-letter using raw parameters.

    Convenience wrapper for dead-lettering without a ConsumeResult object.

    Args:
        event_id: Original event identifier.
        event_type: Original event type.
        payload: Original event payload.
        source: Original event source.
        failure_reason: Why processing failed.
        retry_count: Number of retries attempted.
        project_id: GCP project ID.
        dead_letter_topic_id: Dead-letter topic ID.
        client: Optional pre-configured PublisherClient.

    Returns:
        DeadLetterRecord with details of the dead-lettered message.
    """
    fake_consume = ConsumeResult(
        event=PubSubEvent(
            event_id=event_id,
            event_type=event_type,
            payload=payload,
            source=source,
        ),
        ack_id="",
        delivery_attempt=retry_count,
    )
    return send_to_dead_letter(fake_consume, failure_reason, project_id, dead_letter_topic_id, client)


def should_dead_letter(delivery_attempt: int, max_retries: int | None = None) -> bool:
    """Determine if a message should be sent to the dead-letter queue.

    Args:
        delivery_attempt: Current delivery attempt number.
        max_retries: Maximum retries before dead-lettering. Uses default if None.

    Returns:
        True if the message should be dead-lettered.
    """
    threshold = max_retries if max_retries is not None else get_max_retries()
    return delivery_attempt >= threshold


if __name__ == "__main__":
    from messaging_models import ConsumeResult, PubSubEvent
    fake_result = ConsumeResult(
        event=PubSubEvent(
            event_type="payment.failed",
            payload={"payment_id": "PAY-999", "error": "timeout"},
            source="payment-service",
        ),
        ack_id="fake-ack-123",
        delivery_attempt=4,
    )
    record = send_to_dead_letter(fake_result, "Processing timeout after max retries")
    print(f"Dead-lettered message {record.original_event_id}: {record.dead_letter_message_id}")
