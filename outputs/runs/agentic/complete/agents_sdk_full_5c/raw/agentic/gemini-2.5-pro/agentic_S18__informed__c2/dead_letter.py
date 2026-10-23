import os
import json
from google.cloud import pubsub_v1

from messaging_client import get_publisher, DLQ_TOPIC_PATH

def send_to_dlq(failed_message_data: bytes, reason: str):
    """
    Publishes a failed message to a dead-letter queue (DLQ) topic.

    Args:
        failed_message_data: The raw data of the message that failed processing.
        reason: A string explaining why the message failed.
    """
    if not DLQ_TOPIC_PATH:
        print("DLQ_TOPIC_ID not configured. Skipping sending to DLQ.")
        return None
        
    publisher = get_publisher()

    future = publisher.publish(
        DLQ_TOPIC_PATH,
        failed_message_data,
        failure_reason=reason,
        original_topic=os.getenv("GCP_PUBSUB_TOPIC_ID", "unknown")
    )
    
    message_id = future.result()
    print(f"Message sent to DLQ topic {DLQ_TOPIC_PATH} with ID: {message_id}")
    return message_id
