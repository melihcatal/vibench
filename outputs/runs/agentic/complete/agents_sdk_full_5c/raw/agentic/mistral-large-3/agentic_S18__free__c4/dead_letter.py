import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import DeadLetterMessage

publisher = get_pubsub_client()
dead_letter_topic_path = publisher.topic_path(
    os.getenv("GOOGLE_CLOUD_PROJECT"), 
    os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-topic")
)

def send_to_dead_letter(original_message: dict, error: str) -> str:
    dead_letter = DeadLetterMessage(
        original_message=original_message,
        error=error
    )
    future = publisher.publish(
        dead_letter_topic_path,
        data=json.dumps(dead_letter.dict()).encode("utf-8")
    )
    return future.result()