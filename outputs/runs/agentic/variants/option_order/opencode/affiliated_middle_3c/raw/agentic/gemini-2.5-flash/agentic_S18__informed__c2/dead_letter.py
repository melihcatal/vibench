import json
from messaging_client import get_publisher_client, get_project_id, get_topic_path
from messaging_models import PubSubMessage


def send_to_dead_letter(
    dead_letter_topic_id: str, original_message: PubSubMessage, error_details: str
):
    publisher = get_publisher_client()
    project_id = get_project_id()
    dead_letter_topic_path = get_topic_path(project_id, dead_letter_topic_id)

    # Add dead-letter specific attributes
    attributes = original_message.attributes.copy()
    attributes["dead_letter_reason"] = error_details
    if original_message.message_id:
        attributes["original_message_id"] = original_message.message_id

    data = original_message.to_json().encode("utf-8")

    future = publisher.publish(dead_letter_topic_path, data, **attributes)
    message_id = future.result()
    print(f"Sent message to dead-letter topic with ID: {message_id}")
    return message_id
