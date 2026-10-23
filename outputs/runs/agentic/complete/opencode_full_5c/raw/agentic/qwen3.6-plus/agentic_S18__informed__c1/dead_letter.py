import os
import json
from google.cloud import pubsub_v1

PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "default-project")
DLQ_TOPIC_ID = os.environ.get("GOOGLE_PUBSUB_DLQ_TOPIC_ID", "events-dlq")

publisher = pubsub_v1.PublisherClient()
dlq_topic_path = publisher.topic_path(PROJECT_ID, DLQ_TOPIC_ID)


def send_to_dead_letter(
    original_message: dict,
    error_reason: str,
    retry_count: int = 0,
    attributes: dict | None = None,
) -> str:
    payload = {
        "original_message": original_message,
        "error_reason": error_reason,
        "retry_count": retry_count,
    }
    data = json.dumps(payload).encode("utf-8")
    attrs = {
        "dlq": "true",
        "original_message_id": original_message.get("message_id", "unknown"),
    }
    if attributes:
        attrs.update({k: str(v) for k, v in attributes.items()})
    future = publisher.publish(dlq_topic_path, data=data, **attrs)
    message_id = future.result()
    return message_id
