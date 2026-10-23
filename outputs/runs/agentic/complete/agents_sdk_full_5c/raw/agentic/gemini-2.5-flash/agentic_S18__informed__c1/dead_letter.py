import json
import os
from google.cloud import pubsub_v1

def send_to_dead_letter_topic(project_id: str, dead_letter_topic_id: str, failed_message_data: dict, original_message_id: str = None):
    """Sends a failed message to a designated dead-letter Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    # Enhance the failed message with context if available
    dead_letter_payload = {
        "original_message_id": original_message_id,
        "failure_reason": "message_processing_failed",
        "failed_data": failed_message_data,
        "timestamp": "2023-10-27T10:05:00Z" # Example timestamp
    }
    json_data = json.dumps(dead_letter_payload)
    message_data = json_data.encode("utf-8")

    # Add an attribute to indicate it's a dead-letter message
    attributes = {"dlq_status": "failed"}
    if original_message_id:
        attributes["original_message_id"] = original_message_id

    future = publisher.publish(dead_letter_topic_path, message_data, **attributes)
    print(f"Sent failed message to dead-letter topic with ID: {future.result()}")

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    dead_letter_topic_id = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID")

    if not project_id or not dead_letter_topic_id:
        print("Please set GOOGLE_CLOUD_PROJECT and PUBSUB_DEAD_LETTER_TOPIC_ID environment variables.")
    else:
        sample_failed_data = {"event_type": "corrupted_event", "error": "invalid_json"}
        original_id = "some-original-message-id-123"
        send_to_dead_letter_topic(project_id, dead_letter_topic_id, sample_failed_data, original_id)
