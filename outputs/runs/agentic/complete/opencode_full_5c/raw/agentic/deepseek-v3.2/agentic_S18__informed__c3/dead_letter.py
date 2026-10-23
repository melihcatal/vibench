import os
import json
from google.cloud import pubsub_v1


def dead_letter(topic_name, message_data, error_reason, original_message_id=None):
    """Send failed messages to a dead-letter topic in Google Cloud Pub/Sub."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    publisher = pubsub_v1.PublisherClient()
    dead_letter_topic_name = f"{topic_name}-dead-letter"
    topic_path = publisher.topic_path(project_id, dead_letter_topic_name)

    dead_letter_payload = {
        "original_message": message_data,
        "error_reason": error_reason,
        "original_message_id": original_message_id,
        "timestamp": os.environ.get("DEAD_LETTER_TIMESTAMP", ""),
    }

    data = json.dumps(dead_letter_payload).encode("utf-8")

    future = publisher.publish(
        topic_path,
        data,
        error_reason=error_reason,
        original_message_id=original_message_id or "",
    )
    message_id = future.result()

    return {
        "message_id": message_id,
        "dead_letter_topic": topic_path,
        "error_reason": error_reason,
    }
