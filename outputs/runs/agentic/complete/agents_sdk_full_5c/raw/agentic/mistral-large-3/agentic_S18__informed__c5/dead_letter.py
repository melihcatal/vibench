from google.cloud import pubsub_v1
import os
from messaging_models import Event
from messaging_client import get_publisher_client

def send_to_dead_letter(topic_id: str, event: Event, error: str) -> str:
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_id)
    
    event.attributes["error"] = error
    event_data = event.model_dump_json().encode("utf-8")
    future = publisher.publish(topic_path, data=event_data, **event.attributes)
    message_id = future.result()
    return message_id