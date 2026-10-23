import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher, get_topic_path
from typing import List

def batch_publish(events: List[dict]) -> List[str]:
    publisher = get_publisher()
    topic_path = get_topic_path()
    futures = []
    for event in events:
        data = json.dumps(event).encode("utf-8")
        future = publisher.publish(topic_path, data)
        futures.append(future)
    message_ids = [future.result() for future in futures]
    return message_ids