import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage

publisher = get_pubsub_client()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
TOPIC_NAME = os.getenv("PUBSUB_TOPIC_NAME", "orders-topic")

def publish_event(event_data: dict) -> str:
    event = EventMessage(**event_data)
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    
    future = publisher.publish(
        topic_path,
        data=json.dumps(event.dict()).encode("utf-8"),
        **event.attributes
    )
    return future.result()