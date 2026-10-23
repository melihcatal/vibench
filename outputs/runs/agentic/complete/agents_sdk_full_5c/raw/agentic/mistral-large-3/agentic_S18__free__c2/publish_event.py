import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventRequest

publisher = get_pubsub_client()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
TOPIC_NAME = os.getenv("PUBSUB_TOPIC_NAME", "orders-v1")

def publish_event(event_data: dict) -> str:
    event_request = EventRequest(**event_data)
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    
    future = publisher.publish(
        topic_path,
        data=json.dumps(event_request.payload).encode("utf-8"),
        **event_request.attributes
    )
    return future.result()