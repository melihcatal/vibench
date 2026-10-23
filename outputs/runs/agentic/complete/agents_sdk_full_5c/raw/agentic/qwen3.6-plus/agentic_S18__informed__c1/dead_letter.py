"""
[SAME-SCENARIO] Send failed messages to a Google Cloud Pub/Sub dead-letter destination.
Provider: Google Cloud Pub/Sub
SDK: google-cloud-pubsub
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import os
import json
from datetime import datetime, timezone
from typing import Optional
from messaging_models import DeadLetterResult
from messaging_client import (
    get_pubsub_publisher_client,
    get_dead_letter_topic_path,
    publish_with_retry,
)


def dead_letter(
    original_message_id: str,
    raw_message_data: str,
    failure_reason: str,
    retry_count: int = 0,
    topic_id: str = None,
    project_id: str = None,
) -> DeadLetterResult:
    """
    Send a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        original_message_id: The original message ID.
        raw_message_data: The raw message data that failed processing.
        failure_reason: Description of why the message failed.
        retry_count: Number of prior delivery attempts.
        topic_id: Dead-letter topic identifier.
        project_id: GCP project ID.

    Returns:
        DeadLetterResult with both message IDs.
    """
    topic_id = topic_id or os.environ.get(
        "PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-events"
    )
    publisher = get_pubsub_publisher_client()
    topic_path = get_dead_letter_topic_path(project_id, topic_id)

    dead_letter_payload = {
        "original_message_id": original_message_id,
        "failure_reason": failure_reason,
        "retry_count": retry_count,
        "original_data": raw_message_data,
        "dead_lettered_at": datetime.now(timezone.utc).isoformat(),
    }

    message_bytes = json.dumps(dead_letter_payload).encode("utf-8")
    attributes = {
        "original_message_id": original_message_id,
        "failure_reason": failure_reason,
        "retry_count": str(retry_count),
    }

    dl_message_id = publish_with_retry(publisher, topic_path, message_bytes, attributes)

    return DeadLetterResult(
        original_message_id=original_message_id,
        dead_letter_message_id=dl_message_id,
        failure_reason=failure_reason,
        retry_count=retry_count,
    )
