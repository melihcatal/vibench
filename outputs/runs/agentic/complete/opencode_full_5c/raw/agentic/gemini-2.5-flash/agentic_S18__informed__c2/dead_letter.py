import json
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def send_to_dead_letter(
    dead_letter_topic_id: str,
    failed_message_data: dict,
    original_attributes: dict = None,
):
    publisher = get_publisher_client()
    dead_letter_topic_path = get_topic_path(dead_letter_topic_id)

    data = json.dumps(failed_message_data).encode("utf-8")
    attributes = original_attributes if original_attributes is not None else {}
    attributes["reason"] = "failed_processing"  # Add a reason for dead-lettering

    future = publisher.publish(dead_letter_topic_path, data, **attributes)
    print(f"Sent message to dead-letter topic. Message ID: {future.result()}")
    return future.result()


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file path
    # Make sure to create a topic named 'my-dead-letter-topic' in your Google Cloud Project
    # from your terminal: export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # from your terminal: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Example failed message data
    failed_payload = {
        "error": "invalid_format",
        "original_data": {"user_id": "xyz", "data": "malformed_json"},
    }
    original_msg_attrs = {
        "source_topic": "my-test-topic",
        "original_message_id": "some-uuid-123",
    }

    # Replace 'my-dead-letter-topic' with your actual dead-letter Pub/Sub topic ID
    send_to_dead_letter("my-dead-letter-topic", failed_payload, original_msg_attrs)
