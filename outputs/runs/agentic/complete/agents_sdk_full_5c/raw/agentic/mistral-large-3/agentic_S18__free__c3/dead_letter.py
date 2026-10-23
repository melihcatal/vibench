import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import DeadLetterMessage

publisher = get_pubsub_client()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
DEAD_LETTER_TOPIC = os.getenv("PUBSUB_DEAD_LETTER_TOPIC", "dead-letter-topic")

def send_to_dead_letter(message: dict, error: str) -> str:
    dead_letter = DeadLetterMessage(
        original_message=message,
        error=error
    )
    topic_path = publisher.topic_path(PROJECT_ID, DEAD_LETTER_TOPIC)
    
    future = publisher.publish(
        topic_path,
        data=json.dumps(dead_letter.dict()).encode("utf-8"),
        error=error
    )
    return future.result()