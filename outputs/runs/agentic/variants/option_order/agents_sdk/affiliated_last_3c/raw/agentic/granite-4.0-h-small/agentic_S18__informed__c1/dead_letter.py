# dead_letter.py
# [SAME-SCENARIO]
# Send a failed Pub/Sub message to a dead-letter topic.

import os
from google.cloud import pubsub_v1
from .messaging_client import get_publisher_client
from .messaging_models import EventMessage

def dead_letter_message(original_topic: str, message: EventMessage, dlq_topic: str) -> str:
    """Forward the given message to a designated dead-letter-topic.

    Args:
        original_topic: Name of the source topic where the original publish failed.
        message: EventMessage instance to re‑publish.
        dlq_topic: Name of the dead‑letter topic.
    Returns:
        The message ID assigned by Pub/Sub to the DLQ publish.
    """
    publisher = get_publisher_client()
    dlq_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/topics/{dlq_topic}"
    data = message.to_json()
    future = publisher.publish(dlq_name, data.encode('utf-8'))
    return future.result()
