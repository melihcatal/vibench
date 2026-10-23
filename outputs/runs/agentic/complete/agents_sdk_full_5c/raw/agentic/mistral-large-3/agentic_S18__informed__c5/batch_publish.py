from google.cloud import pubsub_v1
import os
from typing import List
from messaging_models import Event
from messaging_client import get_publisher_client

def batch_publish(topic_id: str, events: List[Event]) -> List[str]:
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id)
    
    futures = []
    for event in events:
        event_data = event.model_dump_json().encode("utf-8")
        future = publisher.publish(topic_path, data=event_data, **event.attributes)
        futures.append(future)
    
    return [future.result() for future in futures]