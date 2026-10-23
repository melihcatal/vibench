import json
import os
from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage


def publish_json_event(topic_id: str, message: PubSubMessage) -> str:
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, topic_id)

    data_json = message.to_json()
    data = data_json.encode("utf-8")

    future = publisher.publish(topic_path, data, **(message.attributes or {}))
    message_id = future.result()
    return message_id
