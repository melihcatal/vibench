import json
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import MessagePayload


def publish_event(topic_id: str, event: MessagePayload):
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    data = json.dumps(event).encode("utf-8")

    future = publisher.publish(topic_path, data)
    return future.result()
