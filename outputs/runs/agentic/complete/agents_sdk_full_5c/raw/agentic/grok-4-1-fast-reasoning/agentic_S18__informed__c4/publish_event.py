import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher, get_topic_path

def publish_event(event: dict) -> str:
    publisher = get_publisher()
    topic_path = get_topic_path()
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()
    return message_id