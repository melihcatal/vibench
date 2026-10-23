from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage
import json


def publish_json_event(topic_id: str, event_data: dict, attributes: dict = None):
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, topic_id)

    message = PubSubMessage(event_data, attributes=attributes)
    future = publisher.publish(
        topic_path, message.to_json(), **(attributes if attributes else {})
    )
    message_id = future.result()
    return message_id
