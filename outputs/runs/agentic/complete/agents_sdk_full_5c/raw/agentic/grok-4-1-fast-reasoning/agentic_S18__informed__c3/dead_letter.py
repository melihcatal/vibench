import json
import os
from typing import Dict, Any
from google.cloud import pubsub_v1
from messaging_client import GOOGLE_CLOUD_PROJECT, DEAD_LETTER_TOPIC
from messaging_models import Event

def send_to_dead_letter(event_data: Dict[str, Any], reason: str = "") -> str:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GOOGLE_CLOUD_PROJECT, DEAD_LETTER_TOPIC)
    dl_payload = {"original": event_data, "reason": reason}
    event = Event(event_type="dead_letter", payload=dl_payload)
    data = event.to_json().encode("utf-8")
    api_future = publisher.publish(topic_path, data)
    message_id = api_future.result()
    return message_id
