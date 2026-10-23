import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import BatchEventRequest

publisher = get_pubsub_client()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
TOPIC_NAME = os.getenv("PUBSUB_TOPIC_NAME", "orders-v1")

def batch_publish(events: list[dict]) -> list[str]: 
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
    batch = publisher.batch()
    
    message_ids = []
    for event in events:
        event_request = BatchEventRequest(**event)
        future = batch.publish(
            topic_path,
            data=json.dumps(event_request.payload).encode("utf-8"),
            message_id=event_request.message_id,
            **event_request.attributes
        )
        message_ids.append(future.result())
    
    return message_ids