import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher, get_dead_letter_path

def send_to_dead_letter(message_data: dict, attributes: dict = None):
    publisher = get_publisher()
    dead_letter_path = get_dead_letter_path()
    data = json.dumps(message_data).encode("utf-8")
    future = publisher.publish(dead_letter_path, data, **(attributes or {}))
    return future.result()