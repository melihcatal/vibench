import json
from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage


def send_to_dead_letter(
    dead_letter_topic_id: str, message: PubSubMessage, error_reason: str
) -> str:
    publisher = get_publisher_client()
    project_id = get_project_id()
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    # Add dead-letter specific attributes
    attributes = message.attributes or {}
    attributes["dlq_reason"] = error_reason
    attributes["original_message_id"] = message.id if message.id else "unknown"

    data_json = message.to_json()
    data = data_json.encode("utf-8")

    future = publisher.publish(dead_letter_topic_path, data, **attributes)
    message_id = future.result()
    return message_id
