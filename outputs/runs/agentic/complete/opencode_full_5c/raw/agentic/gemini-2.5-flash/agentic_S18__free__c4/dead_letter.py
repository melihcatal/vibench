from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage
import json


def send_to_dead_letter(
    dead_letter_topic_id: str,
    failed_event_data: dict,
    original_message_id: str = None,
    error_details: str = None,
) -> str:
    """Sends a failed message to a designated dead-letter topic.

    Args:
        dead_letter_topic_id: The ID of the dead-letter topic.
        failed_event_data: The dictionary representing the failed event payload.
        original_message_id: Optional ID of the original message that failed.
        error_details: Optional string containing details about the failure.

    Returns:
        The message ID of the published dead-letter message.
    """
    publisher = get_publisher_client()
    project_id = get_project_id()
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    attributes = {"status": "dead-letter"}
    if original_message_id:
        attributes["original_message_id"] = original_message_id
    if error_details:
        attributes["error_details"] = error_details

    message = PubSubMessage(failed_event_data, attributes=attributes)
    data = message.to_json().encode("utf-8")

    future = publisher.publish(dead_letter_topic_path, data, **attributes)
    message_id = future.result()
    return message_id
