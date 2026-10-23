import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage

publisher = get_pubsub_client()
topic_path = publisher.topic_path(os.getenv("GOOGLE_CLOUD_PROJECT"), os.getenv("PUBSUB_TOPIC_ID", "events-topic"))

def publish_event(event_data: dict) -> str:
    event = EventMessage(**event_data)
    future = publisher.publish(
        topic_path,
        data=json.dumps(event.dict()).encode("utf-8"),
        message_id=event.event_id
    )
    return future.result()