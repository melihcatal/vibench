import json
import os
from messaging_client import get_publisher_client, get_topic_path, get_project_id


def send_to_dead_letter(topic_id: str, failed_message_data: dict, error: str):
    """Sends a failed message to a dead-letter topic in Google Cloud Pub/Sub."""
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    publisher = get_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    attributes = {"error": error, "original_payload": json.dumps(failed_message_data)}

    data = b"Failed message"

    future = publisher.publish(topic_path, data, **attributes)
    return future.result()


if __name__ == "__main__":
    # This is an example, and will not be executed.
    DLQ_TOPIC_ID = os.environ.get("PUB_SUB_DLQ_TOPIC", "my-topic-dlq")
    failed_message = {"message": "This message failed processing", "user_id": 67890}
    error_reason = "Invalid message format"

    print(f"Sending failed message to DLQ topic {DLQ_TOPIC_ID}...")
    message_id = send_to_dead_letter(DLQ_TOPIC_ID, failed_message, error_reason)
    print(f"Sent message to DLQ with ID: {message_id}")
