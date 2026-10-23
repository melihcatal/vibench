import json
from typing import Dict, Any
from google.cloud import pubsub_v1
from messaging_client import topic_path, TOPIC_ID
from messaging_models import serialize_event

def publish_event(event: Dict[str, Any]) -> None:
    publisher = pubsub_v1.PublisherClient()
    topic = topic_path(TOPIC_ID)
    data = serialize_event(event)
    future = publisher.publish(topic, data)
    future.result()
