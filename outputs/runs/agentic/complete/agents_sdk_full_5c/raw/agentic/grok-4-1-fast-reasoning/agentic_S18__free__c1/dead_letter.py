from typing import Dict, Any
from google.cloud import pubsub_v1
from messaging_client import topic_path, DLQ_TOPIC_ID
from messaging_models import serialize_event

def send_to_dead_letter(failed_event: Dict[str, Any]) -> None:
    publisher = pubsub_v1.PublisherClient()
    topic = topic_path(DLQ_TOPIC_ID)
    data = serialize_event(failed_event)
    future = publisher.publish(topic, data)
    future.result()
