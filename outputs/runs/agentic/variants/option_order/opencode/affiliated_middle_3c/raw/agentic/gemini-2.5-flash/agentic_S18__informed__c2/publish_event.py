import json
from messaging_client import get_publisher_client, get_project_id, get_topic_path
from messaging_models import PubSubMessage


def publish_event(topic_id: str, event_data: dict, attributes: dict = None):
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = get_topic_path(project_id, topic_id)

    message = PubSubMessage(event_data, attributes=attributes)
    data = message.to_json().encode("utf-8")

    future = publisher.publish(topic_path, data, **message.attributes)
    message_id = future.result()
    print(f"Published message with ID: {message_id}")
    return message_id
