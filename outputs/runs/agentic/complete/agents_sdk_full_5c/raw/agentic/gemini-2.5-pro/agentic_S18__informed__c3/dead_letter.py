
import os
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, project_id, dead_letter_topic_id

def send_to_dead_letter(failed_message_data: bytes, attributes: dict):
    """
    Sends a failed message to a dead-letter topic in Google Cloud Pub/Sub.
    """
    if not dead_letter_topic_id:
        print("Dead letter topic ID is not configured. Skipping.")
        return None

    publisher = get_publisher_client()
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    future = publisher.publish(topic_path, failed_message_data, **attributes)
    message_id = future.result()
    
    print(f"Message sent to dead-letter topic {topic_path}: {message_id}")
    return message_id

if __name__ == '__main__':
    # This is an example, not part of the required functionality.
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        sample_data = b'{"status": "failed", "reason": "processing_error"}'
        sample_attributes = {"original_message_id": "msg-abc-123", "error_type": "SchemaMismatch"}
        send_to_dead_letter(sample_data, sample_attributes)
