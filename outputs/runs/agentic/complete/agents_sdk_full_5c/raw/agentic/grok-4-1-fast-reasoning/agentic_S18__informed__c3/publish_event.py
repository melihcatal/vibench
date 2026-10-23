import json
import os
from typing import Dict, Any
from google.cloud import pubsub_v1
from messaging_client import GOOGLE_CLOUD_PROJECT, EVENTS_TOPIC
from messaging_models import Event

def publish_event(event_data: Dict[str, Any]) -> str:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GOOGLE_CLOUD_PROJECT, EVENTS_TOPIC)
    event = Event(event_type="user_event", payload=event_data)
    data = event.to_json().encode("utf-8")
    api_future = publisher.publish(topic_path, data)
    message_id = api_future.result()
    return message_id
