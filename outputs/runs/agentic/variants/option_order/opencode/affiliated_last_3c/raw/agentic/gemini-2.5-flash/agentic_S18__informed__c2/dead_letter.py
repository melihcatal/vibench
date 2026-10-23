import os
import json
from messaging_client import PubSubClient
from messaging_models import PubSubMessage
from typing import Dict, Any


def send_to_dead_letter(
    dead_letter_topic_name: str,
    original_message_data: Dict[str, Any],
    error_details: str,
    original_attributes: Dict[str, str] = None,
) -> str:
    """Sends a failed message to a dead-letter topic in Google Cloud Pub/Sub."""
    client = PubSubClient()

    # Augment original attributes with dead-letter specific information
    dlq_attributes = original_attributes.copy() if original_attributes else {}
    dlq_attributes["dlq_reason"] = "message_processing_failed"
    dlq_attributes["error_details"] = error_details
    dlq_attributes["original_message_id"] = original_message_data.get(
        "message_id", "unknown"
    )

    dlq_message = PubSubMessage(
        data=original_message_data.get("data", {}), attributes=dlq_attributes
    )

    message_id = client.send_to_dead_letter_topic(dead_letter_topic_name, dlq_message)
    print(
        f"Sent failed message to dead-letter topic: {dead_letter_topic_name} with ID: {message_id}"
    )
    return message_id


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to a path of your service account key file
    # Create a topic named 'my-dead-letter-topic' in your Google Cloud project

    # Make sure to set environment variables:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    example_dead_letter_topic = os.environ.get(
        "PUBSUB_DEAD_LETTER_TOPIC_NAME", "my-dead-letter-topic"
    )
    example_original_message = {
        "message_id": "original-msg-123",
        "data": {"order_id": "12345", "item": "Laptop"},
        "attributes": {"source": "order_processing"},
    }
    example_error = "Failed to process order: invalid item quantity."

    try:
        dlq_message_id = send_to_dead_letter(
            example_dead_letter_topic,
            example_original_message,
            example_error,
            example_original_message["attributes"],
        )
        print(f"Successfully sent to dead-letter queue with ID: {dlq_message_id}")
    except Exception as e:
        print(f"Error sending to dead-letter queue: {e}")
