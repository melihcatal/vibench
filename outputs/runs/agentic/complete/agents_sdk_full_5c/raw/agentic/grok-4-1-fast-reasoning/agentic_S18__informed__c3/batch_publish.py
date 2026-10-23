import json
import os
from typing import Dict, Any, List, Optional
from google.cloud import pubsub_v1
from messaging_client import GOOGLE_CLOUD_PROJECT, EVENTS_TOPIC
from messaging_models import Event

def batch_publish(events_data: List[Dict[str, Any]], message_ids: Optional[List[str]] = None) -> List[str]:
    if message_ids is None:
        message_ids = ["" for _ in events_data]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GOOGLE_CLOUD_PROJECT, EVENTS_TOPIC)
    messages = []
    for event_data, msg_id in zip(events_data, message_ids):
        event = Event(event_type="batch_event", payload=event_data)
        data = event.to_json().encode("utf-8")
        attributes = {"batchId": msg_id} if msg_id else {}
        messages.append((data, attributes))
    api_futures = publisher.publish_messages(topic_path, *messages)
    result_ids = [future.result() for future in api_futures]
    return result_ids
