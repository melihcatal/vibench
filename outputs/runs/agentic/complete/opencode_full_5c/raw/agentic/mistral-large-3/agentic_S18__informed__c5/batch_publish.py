from google.cloud import pubsub_v1
import os
import json
from typing import List, Dict, Any
from messaging_models import Event

publisher = pubsub_v1.PublisherClient()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
topic_id = os.getenv("GOOGLE_PUBSUB_TOPIC_ID")


def batch_publish(events: List[Dict[str, Any]]) -> List[str]:
    topic_path = publisher.topic_path(project_id, topic_id)
    message_ids = []

    for event_data in events:
        event = Event(**event_data).dict()
        data = json.dumps(event).encode("utf-8")
        future = publisher.publish(topic_path, data)
        message_ids.append(future.result())

    return message_ids
