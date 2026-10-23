from google.cloud import pubsub_v1
import os
import json

def send_to_dead_letter_queue(project_id: str, dlq_topic_id: str, failed_message_data: dict, original_message_id: str = None):
    """Sends a failed message to a Pub/Sub dead-letter topic."""
    publisher = pubsub_v1.PublisherClient()
    dlq_topic_path = publisher.topic_path(project_id, dlq_topic_id)

    dlq_payload = {
        "original_message_id": original_message_id,
        "failure_reason": "processing_error",
        "failed_data": failed_message_data,
        "timestamp": "2023-10-27T10:30:00Z"
    }

    json_data = json.dumps(dlq_payload)
    message_data = json_data.encode("utf-8")

    future = publisher.publish(dlq_topic_path, message_data)
    print(f"Sent failed message to DLQ. Published message ID: {future.result()}")
    return future.result()

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    DLQ_TOPIC_ID = os.getenv("PUBSUB_DLQ_TOPIC_ID", "my-dlq-topic")

    # Simulate a failed message
    failed_event = {
        "event_id": "failed-event-999",
        "type": "order_processed",
        "data": {"order_id": "ORD-XYZ-789", "status": "failed", "error": "database_timeout"}
    }
    original_msg_id = "abc-123-original-message" # Assuming we know the original message ID

    send_to_dead_letter_queue(PROJECT_ID, DLQ_TOPIC_ID, failed_event, original_msg_id)
