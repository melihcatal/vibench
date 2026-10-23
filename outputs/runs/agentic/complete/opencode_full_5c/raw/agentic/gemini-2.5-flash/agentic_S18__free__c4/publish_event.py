from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage
import json


def publish_event(topic_id: str, event_data: dict, attributes: dict = None) -> str:
    """Publishes a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        topic_id: The ID of the Pub/Sub topic.
        event_data: The dictionary representing the event payload.
        attributes: Optional dictionary of attributes to attach to the message.

    Returns:
        The message ID of the published message.
    """
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, topic_id)

    message = PubSubMessage(event_data, attributes=attributes)
    data = message.to_json().encode("utf-8")

    future = publisher.publish(topic_path, data, **(attributes or {}))
    message_id = future.result()
    return message_id
