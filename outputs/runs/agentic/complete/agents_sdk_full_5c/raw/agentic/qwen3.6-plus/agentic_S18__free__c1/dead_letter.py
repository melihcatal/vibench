"""dead_letter.py - Sends failed messages to a Google Cloud Pub/Sub dead-letter topic."""

import json
import logging
from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError
from messaging_client import (
    get_pubsub_publisher_client,
    PUBSUB_DEAD_LETTER_TOPIC_ID,
    PUBSUB_PROJECT_ID,
)
from messaging_models import PubSubDeadLetterRequest, PubSubDeadLetterResponse

logger = logging.getLogger(__name__)


def send_to_dead_letter(
    original_message_id: str,
    failed_payload: dict,
    failure_reason: str,
    original_attributes: dict = None,
) -> PubSubDeadLetterResponse:
    """Send a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        original_message_id: The message_id of the original failed message.
        failed_payload: The original message payload that failed processing.
        failure_reason: Description of why the message failed.
        original_attributes: Optional original message attributes.

    Returns:
        PubSubDeadLetterResponse with dead-letter message_id and status.
    """
    publisher = get_pubsub_publisher_client()
    dead_letter_topic_path = publisher.topic_path(
        PUBSUB_PROJECT_ID, PUBSUB_DEAD_LETTER_TOPIC_ID
    )

    dead_letter_payload = {
        "original_message_id": original_message_id,
        "original_payload": failed_payload,
        "failure_reason": failure_reason,
        "original_attributes": original_attributes or {},
        "dead_letter_timestamp": "2024-01-15T10:35:00Z",
    }

    attributes = {
        "event_type": "dead_letter",
        "content_type": "application/json",
        "original_message_id": original_message_id,
        "failure_reason": failure_reason[:256],
    }

    request = PubSubDeadLetterRequest(
        topic_path=dead_letter_topic_path,
        payload=dead_letter_payload,
        attributes=attributes,
    )

    try:
        future = publisher.publish(
            request.topic_path,
            json.dumps(request.payload).encode("utf-8"),
            **request.attributes,
        )
        dl_message_id = future.result(timeout=30)

        logger.info(
            "Sent dead-letter message_id=%s to %s",
            dl_message_id,
            dead_letter_topic_path,
        )
        return PubSubDeadLetterResponse(
            dead_letter_message_id=dl_message_id,
            original_message_id=original_message_id,
            status="dead_lettered",
            topic_name=dead_letter_topic_path,
        )

    except GoogleAPIError as exc:
        logger.error("Failed to send dead-letter to Pub/Sub: %s", exc)
        return PubSubDeadLetterResponse(
            dead_letter_message_id=None,
            original_message_id=original_message_id,
            status="failed",
            topic_name=dead_letter_topic_path,
            error=str(exc),
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = send_to_dead_letter(
        original_message_id="msg_orig_123",
        failed_payload={"user_id": "usr_9923", "action": "process_payment"},
        failure_reason="Payment gateway timeout after 3 retries",
        original_attributes={"source": "payment_service"},
    )
    print(f"Dead-letter result: {result}")
