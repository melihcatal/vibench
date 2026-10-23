from google.cloud import pubsub_v1
import json
import os
from messaging_models import Event
from messaging_client import get_publisher_client

def publish_event(topic_id: str, event: Event) -> str:
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id)
    
    event_data = event.model_dump_json().encode("utf-8")
    future = publisher.publish(topic_path, data=event_data, **event.attributes)
    message_id = future.result()
    return message_id