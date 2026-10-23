import json
import os
from google.cloud import pubsub_v1

from messaging_client import get_publisher_client

def send_to_dead_letter_topic(dlq_topic_id: str, message_data: bytes, attributes: dict, project_id: str = None):
    """Sends a failed message to a dead-letter topic in Google Cloud Pub/Sub."""
    publisher = get_publisher_client()
    dlq_topic_path = publisher.topic_path(project_id or os.getenv("GOOGLE_CLOUD_PROJECT"), dlq_topic_id)

    future = publisher.publish(dlq_topic_path, message_data, **attributes)
    print(f"Sent message to DLQ. Message ID: {future.result()}")

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var set)
    # Ensure a topic named 'my-dlq-topic' exists in your project.
    # from your shell, run:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # python dead_letter.py
    failed_message_payload = json.dumps({"error": "processing_failed", "original_data": {"key": "value"}}).encode("utf-8")
    failed_message_attributes = {"reason": "invalid_payload", "original_message_id": "some-uuid-123"}
    send_to_dead_letter_topic("my-dlq-topic", failed_message_payload, failed_message_attributes)
