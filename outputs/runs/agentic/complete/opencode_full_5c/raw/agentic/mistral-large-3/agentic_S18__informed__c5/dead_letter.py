from google.cloud import pubsub_v1
import os
import json
from typing import Dict, Any
from messaging_models import Event

publisher = pubsub_v1.PublisherClient()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
dead_letter_topic_id = os.getenv("GOOGLE_PUBSUB_DEAD_LETTER_TOPIC_ID")


def dead_letter(message_data: Dict[str, Any], error: str) -> str:
    topic_path = publisher.topic_path(project_id, dead_letter_topic_id)
    message_data["error"] = error
    event = Event(**message_data).dict()
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()
    return message_id
