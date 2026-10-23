import json
from typing import List
from google.cloud import pubsub_v1
from messaging_client import get_publisher, get_topic_path

def batch_publish(events: List[dict]):
    publisher = get_publisher()
    topic_path = get_topic_path()
    messages = [json.dumps(event).encode("utf-8") for event in events]
    futures = publisher.publish(topic_path, *messages)
    message_ids = [future.result() for future in futures]
    return message_ids