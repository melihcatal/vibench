import json
from typing import Dict, Any, List
from google.cloud import pubsub_v1
from messaging_client import PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID

def batch_publish(events: List[Dict[str, Any]]) -> List[str]:
    """
    Publishes a batch of messages with IDs to the Pub/Sub topic.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID)
    message_ids = []
    for event in events:
        data = json.dumps(event).encode("utf-8")
        future = publisher.publish(topic_path, data=data)
        message_ids.append(future.result())
    return message_ids