from google.cloud import pubsub_v1
import os
import json

# Load configuration from environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
dead_letter_topic_id = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID")

# Initialize Pub/Sub publisher client for dead-letter topic
publisher = pubsub_v1.PublisherClient()
dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)


def dead_letter(message_data: dict, error_details: str) -> str:
    """
    Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        message_data: Dictionary containing the original message data.
        error_details: String describing the error that occurred.

    Returns:
        str: The message ID of the published dead-letter message.
    """
    # Add error details to the message
    message_data["error_details"] = error_details

    # Serialize message data to JSON
    data = json.dumps(message_data).encode("utf-8")

    # Publish the message to the dead-letter topic
    future = publisher.publish(dead_letter_topic_path, data)
    message_id = future.result()

    return message_id
