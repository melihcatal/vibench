from google.cloud import pubsub_v1
import os
import json

# Load configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
dead_letter_topic_id = os.getenv("GOOGLE_CLOUD_DEAD_LETTER_TOPIC_ID")

# Initialize Pub/Sub publisher client for dead-letter topic
publisher = pubsub_v1.PublisherClient()
dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)


def dead_letter(message_data: dict, error_message: str) -> str:
    """
    Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        message_data: The original message data that failed processing.
        error_message: Description of the error that occurred.

    Returns:
        str: The message ID of the published dead-letter message.
    """
    # Enhance the message with error details
    dead_letter_data = {
        "original_message": message_data,
        "error": error_message,
        "timestamp": os.getenv("TIMESTAMP", str(os.time.time())),
    }

    # Convert to JSON string
    data = json.dumps(dead_letter_data).encode("utf-8")

    # Publish to dead-letter topic
    future = publisher.publish(dead_letter_topic_path, data)
    message_id = future.result()

    return message_id
