from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage


def send_to_dead_letter(
    dead_letter_topic_id: str, failed_message: PubSubMessage, error_details: str
):
    publisher = get_publisher_client()
    project_id = get_project_id()
    dead_letter_topic_path = publisher.topic_path(project_id, dead_letter_topic_id)

    # Add error details to attributes or payload
    attributes = failed_message.attributes.copy() if failed_message.attributes else {}
    attributes["dlq_error"] = error_details

    future = publisher.publish(
        dead_letter_topic_path, failed_message.to_json(), **attributes
    )
    message_id = future.result()
    return message_id
