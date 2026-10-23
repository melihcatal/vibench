import os
from google.cloud import pubsub_v1
import json
from typing import Dict, Any


def send_to_dead_letter(
    message_data: Dict[str, Any], error_reason: str, dead_letter_topic_id: str = None
) -> str:
    """Send failed messages to Google Cloud Pub/Sub dead-letter topic."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    if dead_letter_topic_id is None:
        dead_letter_topic_id = os.environ.get(
            "DEAD_LETTER_TOPIC_ID", "dead-letter-events"
        )

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    dead_letter_message = {
        "original_message": message_data,
        "error_reason": error_reason,
        "failed_at": "2024-01-15T10:30:00Z",
    }

    data = json.dumps(dead_letter_message).encode("utf-8")

    future = publisher.publish(
        topic_path, data, error_reason=error_reason, message_type="dead_letter"
    )
    message_id = future.result()

    return message_id


if __name__ == "__main__":
    sample_failed_message = {
        "event_type": "payment_failed",
        "customer_id": "cust_12345",
        "amount": 99.99,
        "timestamp": "2024-01-15T10:25:00Z",
    }

    error_reason = "Payment processor timeout"

    try:
        message_id = send_to_dead_letter(sample_failed_message, error_reason)
        print(f"Sent to dead letter with message ID: {message_id}")
    except Exception as e:
        print(f"Failed to send to dead letter: {e}")
