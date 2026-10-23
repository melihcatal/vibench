from messaging_client import get_publisher_client, get_topic_name
from messaging_models import normalize_event_payload
from typing import Any, Dict

def send_to_dead_letter(dead_letter_topic_id: str, failed_message_data: Dict[str, Any]):
    """Sends a failed message to a Google Cloud Pub/Sub dead-letter topic.

    Args:
        dead_letter_topic_id: The ID of the dead-letter Pub/Sub topic.
        failed_message_data: A dictionary representing the failed message payload.

    Returns:
        A future object for the publish operation.
    """
    publisher = get_publisher_client()
    dead_letter_topic_path = get_topic_name(dead_letter_topic_id)
    data = normalize_event_payload(failed_message_data)

    future = publisher.publish(dead_letter_topic_path, data)
    return future
