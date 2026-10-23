from google.cloud import pubsub_v1
import os
import json

def send_to_dead_letter(project_id: str, topic_id: str, message_data: dict, message_attributes: dict = None):
    """Sends a failed message to a dead-letter topic.

    Args:
        project_id: The Google Cloud project ID.
        topic_id: The ID of the dead-letter topic.
        message_data: The message payload as a dictionary.
        message_attributes: Optional dictionary of message attributes.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    data = json.dumps(message_data).encode("utf-8")

    future = publisher.publish(topic_path, data, **(message_attributes or {}))
    print(f"Published message ID: {future.result()}")

if __name__ == '__main__':
    # Example usage (replace with your actual project and topic IDs)
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    DEAD_LETTER_TOPIC_ID = os.getenv("DEAD_LETTER_TOPIC_ID")

    if not PROJECT_ID or not DEAD_LETTER_TOPIC_ID:
        print("Please set GOOGLE_CLOUD_PROJECT_ID and DEAD_LETTER_TOPIC_ID environment variables.")
    else:
        failed_message_payload = {"error": "Processing failed", "original_message": {"key": "value"}}
        failed_message_attrs = {"reason": "invalid_format", "timestamp": "2026-09-20T10:00:00Z"}
        send_to_dead_letter(PROJECT_ID, DEAD_LETTER_TOPIC_ID, failed_message_payload, failed_message_attrs)
