from typing import List, Dict, Any
from google.cloud import pubsub_v1
from messaging_client import topic_path, TOPIC_ID
from messaging_models import serialize_event

def batch_publish(events: List[Dict[str, Any]]) -> None:
    publisher = pubsub_v1.PublisherClient()
    topic = topic_path(TOPIC_ID)
    futures = []
    for event in events:
        data = serialize_event(event)
        attributes = event.get("attributes", {}) if isinstance(event.get("attributes"), dict) else {}
        future = publisher.publish(topic, data=data, **attributes)
        futures.append(future)
    for future in futures:
        future.result()
