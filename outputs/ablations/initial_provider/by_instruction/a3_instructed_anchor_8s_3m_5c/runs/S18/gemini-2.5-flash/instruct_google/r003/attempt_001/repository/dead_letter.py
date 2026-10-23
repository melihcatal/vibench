from google.cloud import pubsub_v1
import os
import json

def send_to_dead_letter(project_id: str, dead_letter_topic_id: str, message: dict, original_message_id: str) -> str:
    """Sends a failed message to a designated dead-letter topic in Google Cloud Pub/Sub."""
    publisher = pubsub_v1.PublisherClient()
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    message_json = json.dumps(message).encode("utf-8")
    
    # Add an attribute to indicate the original message ID
    attributes = {"original_message_id": original_message_id, "failure_reason": "simulated_processing_failure"}

    future = publisher.publish(dead_letter_topic_path, message_json, **attributes)
    return future.result()

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    DEAD_LETTER_TOPIC_ID = os.getenv("GOOGLE_CLOUD_PUBSUB_DEAD_LETTER_TOPIC_ID")

    if not PROJECT_ID or not DEAD_LETTER_TOPIC_ID:
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_PUBSUB_DEAD_LETTER_TOPIC_ID environment variables.")
    else:
        failed_message = {"event": "failed_event", "data": "This message failed processing."}
        original_id = "some-original-message-id-123"
        message_id = send_to_dead_letter(PROJECT_ID, DEAD_LETTER_TOPIC_ID, failed_message, original_id)
        print(f"Sent failed message to dead-letter topic with ID: {message_id}")
