import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import DeadLetterRequest

publisher = get_pubsub_client()
dead_letter_topic = publisher.topic_path(
    os.getenv("GOOGLE_CLOUD_PROJECT"), 
    os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-topic")
)

def send_to_dead_letter(message_data: dict, error: str) -> str:
    request = DeadLetterRequest(
        original_message=message_data,
        error=error
    )
    future = publisher.publish(
        dead_letter_topic,
        data=json.dumps(request.dict()).encode("utf-8")
    )
    return future.result()