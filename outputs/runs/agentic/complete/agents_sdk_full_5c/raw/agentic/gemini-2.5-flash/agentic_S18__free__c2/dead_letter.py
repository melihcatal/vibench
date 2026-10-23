from google.cloud import pubsub_v1
import os
import json

def send_to_dead_letter_topic(project_id: str, dead_letter_topic_id: str, failed_message_data: dict, error_reason: str = "") -> str:
    """Sends a failed message to a designated dead-letter Pub/Sub topic.
    In a real-world scenario, Pub/Sub subscriptions handle dead-lettering automatically
    based on configuration. This function demonstrates a manual approach for integration purposes.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    # Add error context to the message for debugging
    dead_letter_payload = {
        "original_message": failed_message_data,
        "error_reason": error_reason,
        "timestamp": "2023-10-27T10:30:00Z" # In a real app, use current timestamp
    }
    
    data_str = json.dumps(dead_letter_payload)
    data = data_str.encode("utf-8")

    future = publisher.publish(topic_path, data)
    message_id = future.result()
    return message_id

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    DEAD_LETTER_TOPIC_ID = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "my-dead-letter-topic")
    failed_event = {"message": "This message failed processing", "id": "msg-123"}
    
    # print(f"Sending failed event to {DEAD_LETTER_TOPIC_ID}...")
    # message_id = send_to_dead_letter_topic(PROJECT_ID, DEAD_LETTER_TOPIC_ID, failed_event, "Invalid format")
    # print(f"Sent dead-letter message with ID: {message_id}")
