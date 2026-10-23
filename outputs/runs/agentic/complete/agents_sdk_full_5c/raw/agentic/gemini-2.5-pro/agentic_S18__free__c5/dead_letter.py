
import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client

def send_to_dead_letter_topic(failed_message_data: bytes, reason: str):
    """
    Publishes a failed message to a dead-letter topic in Google Cloud Pub/Sub.

    Args:
        failed_message_data: The raw data of the message that failed processing.
        reason: A string explaining why the message failed.
    """
    publisher = get_publisher_client()
    project_id = os.environ["GCP_PROJECT_ID"]
    dead_letter_topic_id = os.environ["GCP_DEAD_LETTER_TOPIC_ID"]
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    # Add failure reason as an attribute
    attributes = {"failure_reason": reason}

    future = publisher.publish(topic_path, failed_message_data, **attributes)

    try:
        message_id = future.result()
        print(f"Message sent to dead-letter topic {dead_letter_topic_id} with ID: {message_id}")
        return message_id
    except Exception as e:
        print(f"Failed to send message to dead-letter topic: {e}")
        return None

if __name__ == '__main__':
    # Example Usage:
    # Set the following environment variables before running:
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # export GCP_DEAD_LETTER_TOPIC_ID="your-dead-letter-topic-id"
    
    # Simulating a failed message
    # failed_msg_payload = {
    #     "event_id": "failed-event-123",
    #     "user_id": "user_456",
    #     "data": {"status": "failed", "details": "Invalid format"}
    # }
    # failed_data = json.dumps(failed_msg_payload).encode("utf-8")
    # failure_reason = "JSON schema validation failed"
    
    # send_to_dead_letter_topic(failed_data, failure_reason)
    pass
