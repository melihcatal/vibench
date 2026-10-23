import json
import os
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import EventMessage

publisher = get_pubsub_client()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
DEAD_LETTER_TOPIC_ID = os.getenv("GOOGLE_PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-events")

def send_to_dead_letter(event: EventMessage, error: str) -> str:
    topic_path = publisher.topic_path(PROJECT_ID, DEAD_LETTER_TOPIC_ID)
    
    event.attributes["error"] = error
    
    future = publisher.publish(
        topic_path,
        data=json.dumps(event.dict()).encode("utf-8"),
        **event.attributes
    )
    return future.result()