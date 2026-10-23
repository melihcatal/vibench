import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage

client = get_pubsub_client()

def send_to_dead_letter(topic_name: str, event: EventMessage, error_details: str) -> str:
    dead_letter_topic = client.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_name)
    event.attributes["error_details"] = error_details
    future = client.publish(dead_letter_topic, event.data.encode("utf-8"), **event.attributes)
    message_id = future.result()
    return message_id