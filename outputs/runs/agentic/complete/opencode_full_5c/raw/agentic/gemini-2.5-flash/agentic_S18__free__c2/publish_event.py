import json
from typing import Dict, Any
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage


def publish_json_event(
    topic_name: str, event_data: Dict[str, Any], attributes: Dict[str, str] = None
) -> str:
    """Publishes a JSON event to a Google Cloud Pub/Sub topic.

    Args:
        topic_name: The name of the Pub/Sub topic.
        event_data: The JSON payload of the event as a dictionary.
        attributes: Optional dictionary of attributes to send with the message.

    Returns:
        The message ID of the published message.
    """
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, topic_name)

    message = PubSubMessage(event_data, attributes=attributes)
    data_bytes = message.to_json()

    future = publisher.publish(topic_path, data_bytes, **message.attributes)
    message_id = future.result()
    return message_id
