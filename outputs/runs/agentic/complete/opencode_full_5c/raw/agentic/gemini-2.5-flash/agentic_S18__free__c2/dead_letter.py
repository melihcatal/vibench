from typing import Dict, Any
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage


def send_to_dead_letter_topic(
    dead_letter_topic_name: str,
    original_message: PubSubMessage,
    error_details: Dict[str, Any],
) -> str:
    """Sends a failed message to a designated dead-letter topic.

    Args:
        dead_letter_topic_name: The name of the dead-letter topic.
        original_message: The original PubSubMessage that failed processing.
        error_details: A dictionary containing details about the processing failure.

    Returns:
        The message ID of the published dead-letter message.
    """
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, dead_letter_topic_name)

    # Combine original message data and error details for the dead-letter message
    dead_letter_data = {
        "original_message_data": original_message.data,
        "original_message_id": original_message.message_id,
        "original_attributes": original_message.attributes,
        "error_details": error_details,
    }

    # Optionally, add attributes to the dead-letter message, e.g., error_code
    dead_letter_attributes = original_message.attributes.copy()
    dead_letter_attributes["dlq_reason"] = error_details.get("reason", "unknown_error")

    dead_letter_message = PubSubMessage(
        dead_letter_data, attributes=dead_letter_attributes
    )
    data_bytes = dead_letter_message.to_json()

    future = publisher.publish(topic_path, data_bytes, **dead_letter_message.attributes)
    message_id = future.result()
    return message_id
