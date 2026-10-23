import os
import json
from messaging_client import get_pubsub_publisher_client
from messaging_models import MessagePayload


def publish_event(project_id: str, topic_id: str, payload: MessagePayload):
    publisher = get_pubsub_publisher_client()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = payload.model_dump_json().encode("utf-8")
    future = publisher.publish(topic_path, data)
    return future.result()
