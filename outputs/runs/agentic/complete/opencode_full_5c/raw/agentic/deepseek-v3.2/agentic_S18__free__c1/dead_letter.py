import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import FailedMessage


def send_to_dead_letter(
    message_data: dict, error_reason: str, original_topic: str = None
) -> str:
    """Send failed messages to Google Cloud Pub/Sub dead-letter topic."""
    if original_topic is None:
        original_topic = os.environ.get("PUBSUB_TOPIC_ID", "customer-events")

    dead_letter_topic = f"{original_topic}-dead-letter"
    publisher, project_id = get_pubsub_client()
    topic_path = publisher.topic_path(project_id, dead_letter_topic)

    failed_message = FailedMessage(
        original_message=message_data,
        error_reason=error_reason,
        original_topic=original_topic,
    )

    serialized_data = json.dumps(failed_message.to_dict()).encode("utf-8")

    future = publisher.publish(
        topic_path,
        serialized_data,
        error_type="processing_failure",
        original_topic=original_topic,
        error_reason=error_reason[:100],
    )

    message_id = future.result()
    print(f"Sent failed message to dead-letter topic {dead_letter_topic}: {message_id}")
    return message_id


def process_with_dead_letter_handling(message_data: dict, processing_func):
    """Process message with automatic dead-letter routing on failure."""
    try:
        result = processing_func(message_data)
        return result
    except Exception as e:
        error_reason = str(e)
        send_to_dead_letter(message_data, error_reason)
        raise


if __name__ == "__main__":
    sample_failed_message = {
        "event_type": "payment_failed",
        "customer_id": 12345,
        "timestamp": "2024-01-15T10:30:00Z",
        "payload": {"order_id": "ORD-789", "error_code": "INSUFFICIENT_FUNDS"},
    }

    def faulty_processor(data):
        raise ValueError("Payment processing failed: Insufficient funds")

    try:
        process_with_dead_letter_handling(sample_failed_message, faulty_processor)
    except Exception as e:
        print(f"Processing failed: {e}")
