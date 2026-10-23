import json
from google.cloud import pubsub_v1
from messaging_client import TOPIC_PATH


def publish_event(event_data: dict) -> str:
    publisher = pubsub_v1.PublisherClient()
    data = json.dumps(event_data).encode("utf-8")
    future = publisher.publish(TOPIC_PATH, data)
    message_id = future.result()
    return message_id
