import json
import os
from typing import Dict, Any

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError

from messaging_client import get_publisher_client, get_topic_path

def send_to_dlq(
    publisher: pubsub_v1.PublisherClient,
    dlq_topic_path: str,
    failed_message_data: bytes,
    error_info: Dict[str, Any],
):
    """Sends a failed message to a dead-letter queue (topic)."""
    try:
        attributes = {
            "error_reason": json.dumps(error_info),
            "original_payload_type": "bytes"
        }
        future = publisher.publish(dlq_topic_path, data=failed_message_data, **attributes)
        message_id = future.result()
        print(f"Sent failed message to DLQ {dlq_topic_path} with message ID {message_id}")
        return message_id
    except GoogleAPICallError as e:
        print(f"Error sending message to DLQ {dlq_topic_path}: {e}")
        raise

if __name__ == '__main__':
    # This is an example and will not be executed in the test environment
    # Required environment variables: GOOGLE_PROJECT_ID, MY_DLQ_TOPIC_ID
    dlq_topic_id = os.environ.get("MY_DLQ_TOPIC_ID")
    if dlq_topic_id:
        client = get_publisher_client()
        path = get_topic_path(dlq_topic_id)
        original_message = b'{"key": "some invalid data"}'
        processing_error = {"code": 500, "message": "Failed to parse JSON."}
        send_to_dlq(client, path, original_message, processing_error)
    else:
        print("MY_DLQ_TOPIC_ID environment variable not set. Skipping example.")
