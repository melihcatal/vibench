from google.cloud import pubsub_v1
import os
import json

def send_to_dead_letter_topic(project_id: str, dead_letter_topic_id: str, original_message_data: dict, error_details: str, original_attributes: dict = None):
    """Sends a failed message to a dead-letter Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    # Package the original message data and error details
    dlq_payload = {
        "original_message": original_message_data,
        "error": error_details,
        "timestamp": os.getenv("MESSAGE_FAILURE_TIMESTAMP", "unknown"),
    }
    data_bytes = json.dumps(dlq_payload).encode("utf-8")

    # Add some attributes to the dead-letter message, including original attributes if any
    dlq_attributes = {"dlq_reason": "processing_failed"}
    if original_attributes:
        dlq_attributes.update(original_attributes)

    future = publisher.publish(dead_letter_topic_path, data_bytes, **dlq_attributes)
    print(f"Sent failed message to DLQ with ID: {future.result()}")
    return future.result()

if __name__ == '__main__':
    # Example usage (simulate a failed message)
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    DEAD_LETTER_TOPIC_ID = "my-dead-letter-topic" # Ensure this topic exists in your GCP project

    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        failed_data = {"id": "msg-123", "content": "problematic content"}
        error_info = "Failed to parse JSON due to invalid format."
        original_attrs = {"original_event_type": "data_ingest"}
        send_to_dead_letter_topic(PROJECT_ID, DEAD_LETTER_TOPIC_ID, failed_data, error_info, original_attrs)
