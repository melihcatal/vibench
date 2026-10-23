"""
Send failed messages to a Google Cloud Pub/Sub dead-letter topic.

Uses the google-cloud-pubsub SDK to route failed messages to a designated
dead-letter topic for later inspection and reprocessing.
Requires GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.
"""

import os
import json
from typing import Optional
from datetime import datetime, timezone

from google.cloud import pubsub_v1

from messaging_models import DeadLetterRecord, ConsumedMessage
from messaging_client import PubSubClientHelper


def send_to_dead_letter(
    original_topic_id: str,
    consumed_message: ConsumedMessage,
    error_reason: str,
    retry_count: int = 0,
    project_id: Optional[str] = None,
) -> DeadLetterRecord:
    """
    Send a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        original_topic_id: The original topic ID (used to derive dead-letter topic name).
        consumed_message: The consumed message that failed processing.
        error_reason: Description of why the message failed.
        retry_count: Number of retry attempts before dead-lettering.
        project_id: Optional GCP project ID.

    Returns:
        DeadLetterRecord describing the dead-lettered message.
    """
    helper = PubSubClientHelper(project_id=project_id)

    dl_topic_id = f"{original_topic_id}-dead-letter"

    dead_letter_record = DeadLetterRecord(
        original_message_id=consumed_message.message_id,
        error_reason=error_reason,
        retry_count=retry_count,
        original_payload=consumed_message.data,
        destination=dl_topic_id,
    )

    dl_payload = {
        "dead_letter_record": dead_letter_record.to_dict(),
        "dead_lettered_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        data = json.dumps(dl_payload).encode("utf-8")
        attributes = {
            "dead_letter": "true",
            "original_message_id": consumed_message.message_id,
            "error_reason": error_reason,
            "retry_count": str(retry_count),
        }

        message_id = helper.publish_message(
            topic_id=dl_topic_id,
            data=data,
            attributes=attributes,
        )

        dead_letter_record.destination = helper.get_dead_letter_topic_path(dl_topic_id)
        return dead_letter_record

    except Exception as e:
        dead_letter_record.error_reason = f"Failed to send to dead-letter: {str(e)}"
        return dead_letter_record
    finally:
        helper.close()


def dead_letter_from_exception(
    original_topic_id: str,
    consumed_message: ConsumedMessage,
    exception: Exception,
    retry_count: int = 0,
    project_id: Optional[str] = None,
) -> DeadLetterRecord:
    """
    Dead-letter a message due to an exception during processing.

    Args:
        original_topic_id: Original topic ID.
        consumed_message: The failed consumed message.
        exception: The exception that caused the failure.
        retry_count: Number of retries attempted.
        project_id: Optional GCP project ID.

    Returns:
        DeadLetterRecord for the failed message.
    """
    return send_to_dead_letter(
        original_topic_id=original_topic_id,
        consumed_message=consumed_message,
        error_reason=f"{type(exception).__name__}: {str(exception)}",
        retry_count=retry_count,
        project_id=project_id,
    )


if __name__ == "__main__":
    from messaging_models import ConsumedMessage

    sample_message = ConsumedMessage(
        message_id="msg_abc123",
        data='{"event_type": "order.create", "payload": {"order_id": "ord_999"}}',
        attributes={"source": "api"},
    )

    result = send_to_dead_letter(
        original_topic_id="events-topic",
        consumed_message=sample_message,
        error_reason="Processing timeout after 3 retries",
        retry_count=3,
    )
    print(json.dumps(result.to_dict(), indent=2))
