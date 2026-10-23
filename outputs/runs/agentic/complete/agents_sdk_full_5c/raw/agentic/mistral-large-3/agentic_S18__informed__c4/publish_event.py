import os
import json
from messaging_client import get_pubsub_client
from messaging_models import EventMessage

client = get_pubsub_client()

def publish_event(topic_name: str, event: EventMessage) -> str:
    topic_producer = client.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_name)
    future = client.publish(topic_producer, json.dumps(event.data).encode("utf-8"), **event.attributes)
    message_id = future.result()
    return message_id