import json
from messaging_client import get_topic_path, get_publisher_client
from messaging_models import MessageEvent


def publish_event(event: MessageEvent, topic_id: str = None) -> str:
    topic_path = get_topic_path(topic_id)
    publisher = get_publisher_client()
    data = json.dumps(event.payload).encode("utf-8")
    future = publisher.publish(topic_path, data=data, **(event.attributes or {}))
    return future.result()
