import json
from typing import Dict, Any
from google.cloud import pubsub_v1
from messaging_client import PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID

def publish_event(event: Dict[str, Any]) -> str:
    """
    Publishes a JSON event to the managed Pub/Sub topic.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID)
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    message_id = future.result()
    return message_id