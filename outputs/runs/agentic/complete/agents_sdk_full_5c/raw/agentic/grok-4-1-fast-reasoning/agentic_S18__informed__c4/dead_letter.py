import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher, get_dead_letter_topic_path

def send_to_dead_letter(event: dict, attributes: dict = None) -> str:
    publisher = get_publisher()
    topic_path = get_dead_letter_topic_path()
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data, **(attributes or {}))
    message_id = future.result()
    return message_id