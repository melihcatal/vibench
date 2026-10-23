import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage

client = get_pubsub_client()

def batch_publish(topic_name: str, events: list[EventMessage]) -> list[str]:
    topic_path = client.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), topic_name)
    batch = client.batch()
    
    for event in events:
        batch.publish(topic_path, event.data.encode("utf-8"), **event.attributes)
    
    response = batch.commit()
    return response.message_ids