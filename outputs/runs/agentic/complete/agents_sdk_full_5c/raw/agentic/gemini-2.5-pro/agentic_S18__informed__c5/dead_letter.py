import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher, DLQ_TOPIC_PATH

def send_to_dlq(failed_message_data: dict, reason: str):
    """Sends a failed message to the Dead-Letter Queue (DLQ) topic."""
    publisher = get_publisher()

    # Add failure reason to the message payload
    dlq_payload = {
        "original_payload": failed_message_data,
        "failure_reason": reason,
    }

    data = json.dumps(dlq_payload).encode("utf-8")

    future = publisher.publish(DLQ_TOPIC_PATH, data)
    
    message_id = future.result()
    print(f"Sent message to DLQ with ID: {message_id}")
    return message_id

