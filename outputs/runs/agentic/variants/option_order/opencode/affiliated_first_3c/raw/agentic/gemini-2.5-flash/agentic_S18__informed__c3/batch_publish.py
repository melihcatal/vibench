import json
from typing import List
from messaging_client import get_publisher_client, get_project_id
from messaging_models import PubSubMessage


def publish_batch_events(topic_id: str, messages: List[PubSubMessage]) -> List[str]:
    publisher = get_publisher_client()
    project_id = get_project_id()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for message in messages:
        data_json = message.to_json()
        data = data_json.encode("utf-8")
        future = publisher.publish(topic_path, data, **(message.attributes or {}))
        futures.append(future)

    message_ids = [future.result() for future in futures]
    return message_ids
