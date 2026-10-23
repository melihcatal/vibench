"""Send failed messages to a Google Cloud Pub/Sub dead-letter destination.

Uses Google Cloud Pub/Sub as the concrete external provider.
"""

from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import (
    get_publisher_client,
    get_dead_letter_topic_path,
    encode_message,
    build_attributes,
)
from messaging_models import EventMessage, DeadLetterEntry, MessageResponse


def send_to_dead_letter(
    event: EventMessage,
    failure_reason: str,
    attempt_count: int = 1,
    dead_letter_topic_path: Optional[str] = None,
    project: Optional[str] = None,
    topic_name: Optional[str] = None,
) -> MessageResponse:
    """Publish a failed message to the Google Cloud Pub/Sub dead-letter topic.

    Args:
        event: The original EventMessage that failed.
        failure_reason: Description of why the message failed.
        attempt_count: Number of processing attempts before dead-lettering.
        dead_letter_topic_path: Optional fully-qualified dead-letter topic path.
        project: Optional GCP project ID override.
        topic_name: Optional dead-letter topic name override.

    Returns:
        MessageResponse indicating success or failure.
    """
    try:
        publisher = get_publisher_client()
        topic = dead_letter_topic_path or get_dead_letter_topic_path(
            project=project, topic_name=topic_name
        )

        dead_letter = DeadLetterEntry(
            original_message=event,
            failure_reason=failure_reason,
            attempt_count=attempt_count,
        )

        message_data = dead_letter.to_dict()
        encoded_data = encode_message(message_data)

        attrs = build_attributes({
            "dead_letter_id": dead_letter.dead_letter_id,
            "original_event_id": event.event_id,
            "original_event_type": event.event_type,
            "failure_reason": failure_reason,
            "attempt_count": str(attempt_count),
        })

        future = publisher.publish(topic, encoded_data, **attrs)
        message_id = future.result()

        return MessageResponse(
            success=True,
            message_id=message_id,
            event_id=event.event_id,
            details={
                "dead_letter_id": dead_letter.dead_letter_id,
                "dead_letter_topic": topic,
                "attempt_count": attempt_count,
                "publisher_class": "pubsub_v1.PublisherClient",
            },
        )
    except Exception as exc:
        return MessageResponse(
            success=False,
            event_id=event.event_id,
            error=str(exc),
        )


def dead_letter_from_response(
    event: EventMessage,
    error: str,
    attempt_count: int = 1,
    dead_letter_topic_path: Optional[str] = None,
) -> MessageResponse:
    """Convenience wrapper to dead-letter a message given an error string.

    Args:
        event: The original EventMessage.
        error: The error that caused the failure.
        attempt_count: Number of attempts before dead-lettering.
        dead_letter_topic_path: Optional dead-letter topic path.

    Returns:
        MessageResponse from the dead-letter operation.
    """
    return send_to_dead_letter(
        event=event,
        failure_reason=error,
        attempt_count=attempt_count,
        dead_letter_topic_path=dead_letter_topic_path,
    )
