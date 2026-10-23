import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher, get_topic_path

def publish_event(event_data: dict, attributes: dict = None):
    publisher = get_publisher()
    topic_path = get_topic_path()
    message_data = json.dumps(event_data).encode("utf-8")
    future = publisher.publish(topic_path, message_data, **(attributes or {}))
    message_id = future.result()
    return message_id