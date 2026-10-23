"""Send failed messages to a Google Cloud Pub/Sub dead-letter topic.

Uses the google-cloud-pubsub SDK to publish messages that failed processing
to a designated dead-letter queue for later inspection and reprocessing.
"""

import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from google.cloud import pubsub_v1


def send_to_dead_letter(
    original_message: Dict[str, Any],
    error_reason: str,
    dead_letter_topic_path: Optional[str] = None,
    attempt_count: int = 1,
    attributes: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Send a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        original_message: The original message payload that failed processing.
        error_reason: Description of why the message failed.
        dead_letter_topic_path: Full path to the dead-letter topic.
        attempt_count: Number of processing attempts before dead-lettering.
        attributes: Additional attributes for the dead-letter message.

    Returns:
        Dict with dead-letter publish result.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "pubsub-project-001")
    dead_letter_topic = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC", "events-dlq")

    if dead_letter_topic_path is None:
        publisher = pubsub_v1.PublisherClient()
        dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic)

    dead_letter_payload = {
        "original_message": original_message,
        "error_reason": error_reason,
        "failure_timestamp": datetime.now(timezone.utc).isoformat(),
        "attempt_count": attempt_count,
        "source": os.environ.get("PUBSUB_SUBSCRIPTION", "unknown"),
    }

    message_body = json.dumps(dead_letter_payload).encode("utf-8")

    msg_attributes = {
        "dead_letter": "true",
        "error_reason": error_reason,
        "attempt_count": str(attempt_count),
        "content_type": "application/json",
    }
    if attributes:
        msg_attributes.update(attributes)

    publisher = pubsub_v1.PublisherClient()
    future = publisher.publish(dead_letter_topic_path, message_body, **msg_attributes)
    message_id = future.result()

    return {
        "status": "dead_lettered",
        "dead_letter_topic": dead_letter_topic_path,
        "message_id": message_id,
        "error_reason": error_reason,
        "attempt_count": attempt_count,
    }


def batch_dead_letter(
    failed_messages: List[Dict[str, Any]],
    dead_letter_topic_path: Optional[str] = None,
    batch_error_reason: str = "batch_processing_failure",
) -> Dict[str, Any]:
    """Send multiple failed messages to a dead-letter topic in one call.

    Args:
        failed_messages: List of dicts with 'message' and optional 'error' keys.
        dead_letter_topic_path: Full path to the dead-letter topic.
        batch_error_reason: Default error reason for all messages.

    Returns:
        Dict with batch dead-letter results.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "pubsub-project-001")
    dead_letter_topic = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC", "events-dlq")

    if dead_letter_topic_path is None:
        publisher = pubsub_v1.PublisherClient()
        dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic)

    publisher = pubsub_v1.PublisherClient()
    futures = []

    for idx, entry in enumerate(failed_messages):
        original = entry.get("message", entry)
        error = entry.get("error", batch_error_reason)

        dl_payload = {
            "original_message": original,
            "error_reason": error,
            "failure_timestamp": datetime.now(timezone.utc).isoformat(),
            "batch_index": idx,
            "batch_id": f"batch-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        }

        message_body = json.dumps(dl_payload).encode("utf-8")
        msg_attributes = {
            "dead_letter": "true",
            "batch_index": str(idx),
            "error_reason": error,
            "content_type": "application/json",
        }

        future = publisher.publish(dead_letter_topic_path, message_body, **msg_attributes)
        futures.append(future)

    results = []
    for future in futures:
        results.append(future.result())

    return {
        "status": "batch_dead_lettered",
        "dead_letter_topic": dead_letter_topic_path,
        "message_ids": results,
        "count": len(results),
    }


if __name__ == "__main__":
    result = send_to_dead_letter(
        original_message={"event_id": "evt-001", "data": "failed_payload"},
        error_reason="Schema validation failed: missing required field 'order_id'",
        attempt_count=3,
    )
    print(json.dumps(result, indent=2))
