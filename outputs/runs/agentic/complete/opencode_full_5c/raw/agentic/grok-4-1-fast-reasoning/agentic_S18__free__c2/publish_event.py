import json
from typing import Dict, Any
from messaging_client import publish_message, get_topic_path
import os

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
topic_id = os.getenv("PUBSUB_TOPIC_ID", "events-topic")


def publish_event(event_data: Dict[str, Any]) -> str:
    data = json.dumps(event_data).encode("utf-8")
    return publish_message(topic_id, data)
