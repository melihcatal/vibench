import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_client
from messaging_models import DeadLetterRequest

publisher = get_pubsub_client()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
DEAD_LETTER_TOPIC = os.getenv("PUBSUB_DEAD_LETTER_TOPIC", "dead-letter-orders-v1")

def send_to_dead_letter(dead_letter_request: DeadLetterRequest) -> str:
    topic_path = publisher.topic_path(PROJECT_ID, DEAD_LETTER_TOPIC)
    
    future = publisher.publish(
        topic_path,
        data=json.dumps(dead_letter_request.payload).encode("utf-8"),
        error=dead_letter_request.error,
        original_message_id=dead_letter_request.original_message_id
    )
    return future.result()